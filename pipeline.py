# pipeline.py

class ClovaMultimodalPipeline:
    def __init__(self):
        pass

    def process_image_ocr(self, file_name: str) -> str:
        """CLOVA OCR API: 스크린샷 내 텍스트 추출 시뮬레이션"""
        return f"[OCR 추출 완료] '{file_name}' 이미지 파일에서 대화 텍스트가 정상 추출되었습니다."

    def process_audio_stt(self, file_name: str) -> str:
        """CLOVA Speech API: 음성 파일 텍스트 변환 시뮬레이션"""
        return f"[STT 변환 완료] '{file_name}' 음성 파일이 텍스트로 변환되었습니다."

    def save_to_mybox(self, data_dict: dict) -> bool:
        """네이버 MY BOX 저장 기능 시뮬레이션"""
        return True