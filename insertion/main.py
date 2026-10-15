from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS 설정: 모든 도메인(GAS 웹 앱 포함)에서의 접근을 허용합니다.
CORS(app, resources={r"/sort": {"origins": "*"}})

def insertion_sort_steps(arr):
    """
    단순 삽입 정렬(Insertion Sort)을 수행하면서 각 단계별 상태를 기록하여 반환합니다.
    - arr: 정렬할 숫자 리스트
    - returns: 각 단계별 배열 상태, 현재 비교/삽입 중인 인덱스 등이 담긴 리스트
    """
    steps = []
    n = len(arr)
    
    # 초기 상태 기록
    steps.append({
        "array": list(arr),
        "message": "초기 배열 상태입니다. (첫 번째 원소는 이미 정렬된 것으로 간주)",
        "current_index": 0,
        "comparing_index": -1,
        "sorted_range": [0]
    })
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        
        steps.append({
            "array": list(arr),
            "message": f"인덱스 {i} (값: {key})를 정렬된 부분에 삽입할 위치를 찾습니다.",
            "current_index": i,
            "comparing_index": j,
            "sorted_range": list(range(i))
        })
        
        # 현재 key보다 큰 원소들을 오른쪽으로 한 칸씩 이동
        while j >= 0 and arr[j] > key:
            steps.append({
                "array": list(arr),
                "message": f"인덱스 {j}의 값({arr[j]})이 키값({key})보다 크므로 오른쪽으로 이동합니다.",
                "current_index": i,
                "comparing_index": j,
                "sorted_range": list(range(i))
            })
            
            arr[j + 1] = arr[j]
            j -= 1
            
            if j >= 0:
                steps.append({
                    "array": list(arr),
                    "message": f"다음 비교 대상 인덱스 {j} (값: {arr[j]})를 확인합니다.",
                    "current_index": i,
                    "comparing_index": j,
                    "sorted_range": list(range(i))
                })
        
        # 빈 자리에 key 삽입
        arr[j + 1] = key
        steps.append({
            "array": list(arr),
            "message": f"키값 {key}를 올바른 위치(인덱스 {j + 1})에 삽입했습니다.",
            "current_index": i,
            "comparing_index": j + 1,
            "sorted_range": list(range(i + 1))
        })
        
    # 최종 완료 상태 기록
    steps.append({
        "array": list(arr),
        "message": "단순 삽입 정렬이 성공적으로 완료되었습니다!",
        "current_index": -1,
        "comparing_index": -1,
        "sorted_range": list(range(n))
    })
    return steps

@app.route('/sort', methods=['POST', 'OPTIONS'])
def sort_endpoint():
    """
    클라이언트로부터 숫자들이 담긴 배열을 받아 단순 삽입 정렬 단계별 결과를 반환하는 API 엔드포인트
    """
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON 데이터가 전달되지 않았습니다."}), 400
            
        arr = data.get('array', [12, 11, 13, 5, 6])
        
        # 입력값 검증 (숫자 리스트인지 확인)
        if not isinstance(arr, list) or not all(isinstance(x, (int, float)) for x in arr):
            return jsonify({"error": "유효한 숫자 배열을 전달해주세요."}), 400
            
        steps = insertion_sort_steps(arr)
        
        return jsonify({
            "status": "success",
            "steps": steps,
            "complexity": {
                "time_worst": "O(n^2)",
                "time_best": "O(n)",
                "space": "O(1)"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    """서버 정상 작동 여부를 확인하는 헬스체크 엔드포인트"""
    return jsonify({"status": "online", "message": "Insertion Sort Cloud Run Server is running!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
