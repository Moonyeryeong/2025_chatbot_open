import os
import json

# 사용자 정보 저장 함수 (user_id 기준)
def save_patient_info(user_id: str, data: dict, filename="patient_data.json", overwrite=False):
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", filename)

    # 전체 파일 로드
    try:
        with open(path, "r", encoding="utf-8") as f:
            all_data = json.load(f)
            if not isinstance(all_data, dict):
                all_data = {}
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = {}

    user_records = all_data.get(user_id, [])

    if overwrite:
        if isinstance(data, list):
            all_data[user_id] = data
        else:
            raise ValueError("overwrite=True일 때는 data는 list여야 합니다.")
    else:
        updated = False
        for i, record in enumerate(user_records):
            if (
                record.get("name") == data["name"] and
                record.get("age") == data["age"] and
                record.get("gender") == data["gender"]
            ):
                user_records[i] = data
                updated = True
                break
        if not updated:
            user_records.append(data)
        all_data[user_id] = user_records

    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

# 사용자 정보 불러오기 (user_id 기준)
def load_patient_info(user_id: str, filename="patient_data.json"):
    path = os.path.join("data", filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            all_data = json.load(f)
            return all_data.get(user_id, [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# 사용자 전체 정보 저장 (더 이상 사용되지 않음, 삭제 가능)
def save_all_patient_info(data_list, filename="patient_data.json"):
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

# 복용중인 약 정보 저장 함수 (user_id 기준)
def save_medications(user_id: str, med_list: list, filename="medications.json"):
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", filename)

    print("\n💾 [save_medications] 실행됨")
    print("   사용자 ID:", user_id)
    print("   약 개수:", len(med_list))
    print("   저장 경로:", os.path.abspath(path))

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                data = {}
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[user_id] = med_list

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ 저장 완료!")
    except Exception as e:
        print("❌ 저장 중 오류:", e)

# 복용중인 약 정보 불러오기 함수
def load_medications(user_id: str, filename="medications.json"):
    path = os.path.join("data", filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(user_id, [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

#혈당 불러오기
def load_glucose(user_id: str, filename="glucose.json"):
    path = os.path.join("data", filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(user_id, [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

#초기화
def clear_glucose_data(user_id, filename="glucose.json"):
    path = os.path.join("data", filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = {}

    if user_id in all_data:
        del all_data[user_id]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

def clear_medications_data(user_id, filename="medications.json"):
    path = os.path.join("data", filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_data = {}

    if user_id in all_data:
        del all_data[user_id]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)