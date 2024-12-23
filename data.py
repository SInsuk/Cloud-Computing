import json
import boto3
from urllib import request, parse

def lambda_handler(event, context):
    base_url = "http://apis.data.go.kr/6260000/BusanPblcPrkngInfoService/getPblcPrkngInfo"
    params = {
        "serviceKey": "YOUT_API_KEY",
        "numOfRows": 100,
        "pageNo": 1,
        "resultType": "json"
    }
    
    query_string = parse.urlencode(params)
    url = f"{base_url}?{query_string}"
    
    try:
        with request.urlopen(url) as response:
            response_data = response.read().decode('utf-8')
            print("Response Data:", response_data)  # 응답 내용 로그
            
            # JSON 파싱
            data = json.loads(response_data)
            print("Parsed Data:", data)  # 파싱된 데이터 로그
            
            # DynamoDB 저장 로직...
            return {
                'statusCode': 200,
                'body': json.dumps('Data stored successfully!')
            }
    except Exception as e:
        print("Error:", str(e))  # 에러 로그 추가
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
