import json
from sqlalchemy import text
from app.database import engine
from app.utils.status import normalize_status


def _safe_parse(raw_json):
    """Handles double-encoded ECourt JSON safely"""
    
    if not raw_json or not raw_json.strip():
        return []
    
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        # Try double-encoded
        try:
            data = json.loads(json.loads(raw_json))
        except:
            return []
    
    # Case 1: dict wrapper with safe key extraction
    if isinstance(data, dict):
        data = data.get("data") or data.get("results") or data.get("cases") or []
    
    # Case 2: list of JSON strings (double-encoded)
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], str):
        try:
            return [json.loads(x) for x in data if x and x.strip()]
        except json.JSONDecodeError:
            return []
    
    return data if isinstance(data, list) else []


def import_ecourt_json(raw_json: str, client_id: int = None, filename: str = "unknown"):

    data = _safe_parse(raw_json)

    inserted = 0
    skipped = 0
    duplicates = 0
    invalid = 0

    with engine.begin() as conn:

        for item in data:

            try:
                if not isinstance(item, dict):
                    skipped += 1
                    continue

                cino = item.get("cino") or item.get("case_no") or item.get("case_number")

                if not cino:
                    invalid += 1
                    continue

                # DUP CHECK
                exists = conn.execute(
                    text("SELECT 1 FROM cases WHERE case_number = :c"),
                    {"c": cino}
                ).fetchone()

                if exists:
                    duplicates += 1
                    continue
                
                # CNR uniqueness check (if provided)
                cnr = item.get("cnr") or item.get("cnr_number")
                if cnr:
                    cnr_exists = conn.execute(
                        text("SELECT 1 FROM cases WHERE cnr_number = :c"),
                        {"c": cnr}
                    ).fetchone()
                    if cnr_exists:
                        duplicates += 1
                        continue
                
                title = f"{item.get('petparty_name','')} vs {item.get('resparty_name','')}"

                case_type = item.get("type_name") or item.get("case_type")
                court = item.get("establishment_name") or item.get("court")
                judge = item.get("court_no_desg_name") or item.get("judge")

                status = normalize_status(
                    item.get("disp_name") or item.get("status")
                ).value

                conn.execute(text("""
                    INSERT INTO cases (
                        client_id,
                        case_number,
                        title,
                        case_type,
                        cnr_number,
                        court,
                        judge,
                        status,
                        petitioner,
                        respondent,
                        case_stage,
                        filing_number,
                        filing_year,
                        registration_number,
                        registration_year,
                        ecourts_case_no,
                        establishment_name,
                        establishment_code,
                        description
                    )
                    VALUES (
                        :client_id,
                        :case_number,
                        :title,
                        :case_type,
                        :cnr_number,
                        :court,
                        :judge,
                        :status,
                        :petitioner,
                        :respondent,
                        :case_stage,
                        :filing_number,
                        :filing_year,
                        :registration_number,
                        :registration_year,
                        :ecourts_case_no,
                        :establishment_name,
                        :establishment_code,
                        :description
                    )
                """), {
                    "client_id": client_id or 1,
                    "case_number": cino,
                    "title": title,
                    "case_type": case_type,
                    "cnr_number": item.get("cnr"),
                    "court": court,
                    "judge": judge,
                    "status": status,
                    "petitioner": item.get("petparty_name"),
                    "respondent": item.get("resparty_name"),
                    "case_stage": item.get("case_stage"),
                    "filing_number": item.get("fil_no"),
                    "filing_year": item.get("fil_year"),
                    "registration_number": item.get("reg_no"),
                    "registration_year": item.get("reg_year"),
                    "ecourts_case_no": item.get("case_no"),
                    "establishment_name": item.get("establishment_name"),
                    "establishment_code": item.get("establishment_code"),
                    "description": json.dumps(item)
                })

                inserted += 1

            except Exception:
                skipped += 1

    return {
        "status": "ok",
        "total_input": len(data),
        "inserted": inserted,
        "skipped": skipped,
        "duplicates": duplicates,
        "invalid": invalid
    }