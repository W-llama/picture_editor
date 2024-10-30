from flask import jsonify

class ErrorHandler:
    @staticmethod
    def handle_exception(e, custom_message="An error occurred"):
        """예외 처리와 응답 포맷 통일."""
        print(f"Exception occurred: {str(e)}")
        return jsonify({'error': f'{custom_message}: {str(e)}'}), 500

    @staticmethod
    def client_error(message, status_code=400):
        """클라이언트 오류 처리 (400대 오류)."""
        return jsonify({'error': message}), status_code
