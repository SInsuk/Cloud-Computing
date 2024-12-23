import json
import boto3
import logging
from boto3.dynamodb.conditions import Key

# 로깅 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # DynamoDB 클라이언트 생성
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BusanParking')  # DynamoDB 테이블 이름 설정

    try:
        # 이벤트 로그 기록
        logger.info("Received event: %s", event)
        
        # queryStringParameters 확인 및 값 추출
        query_params = event.get('queryStringParameters') or {}
        mgntNum = query_params.get('mgntNum')

        if mgntNum:
            # mgntNum으로 데이터 조회
            response = table.query(
                KeyConditionExpression=Key('mgntNum').eq(mgntNum)
            )
        else:
            # mgntNum이 없는 경우 전체 데이터 조회
            response = table.scan()

        items = response.get('Items', [])
        data = []

        for item in items:
            doroAddr = item.get("doroAddr", "")
            jibunAddr = item.get("jibunAddr", "Unknown Address")
            address = doroAddr if doroAddr and doroAddr != "-" else jibunAddr  # 주소 설정
            data.append({
                "mgntNum": item.get("mgntNum", ""),
                "pkNam": item.get("pkNam", ""),
                "yCdnt": item.get("yCdnt", ""),
                "xCdnt": item.get("xCdnt", ""),
                "address": address
            })

        # 성공 응답 반환
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
            'body': json.dumps(data)
        }

    except Exception as e:
        logger.error("Error: %s", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # CORS 허용
            },
            'body': json.dumps({'error': str(e)})
        }
