import os
from pathlib import Path

from dotenv import load_dotenv


# backend/.env 파일의 절대 경로
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

# 실행 위치와 관계없이 backend/.env 파일을 불러온다.
load_dotenv(dotenv_path=ENV_PATH)


class AIServiceError(RuntimeError):
    """
    OpenAI API 호출 과정에서 문제가 발생했을 때 사용하는 예외.
    """


class AIConfigurationError(AIServiceError):
    """
    API 키나 모델명 등 환경설정이 잘못된 경우 사용하는 예외.
    """


SYSTEM_INSTRUCTIONS = """
너는 구미 지역 관광 안내 챗봇이다.

사용자의 현재 위치 주변에 있는 관광지를 안내하고,
사용자의 질문에 자연스러운 한국어로 답변한다.

다음 규칙을 반드시 지켜라.

1. 제공된 주변 관광지 정보를 우선적으로 활용한다.
2. 장소를 추천할 때 추천 이유를 함께 설명한다.
3. 사용자 위치와 가까운 장소를 우선 고려한다.
4. 제공되지 않은 운영시간, 입장료, 행사 일정은 추측하지 않는다.
5. 확인할 수 없는 정보는 별도 확인이 필요하다고 안내한다.
6. 주변 장소가 없으면 장소를 임의로 만들어내지 않는다.
7. 답변은 친절하고 이해하기 쉽게 작성한다.
8. 답변은 너무 길지 않게 작성한다.
""".strip()


def get_ai_response(
    user_query: str,
    places_context: str,
) -> str:
    """
    AI_PROVIDER 설정에 따라 Gemini 또는 OpenAI를 호출한다.
    """

    prompt = build_prompt(
        user_query=user_query,
        places_context=places_context,
    )

    provider = os.getenv(
        "AI_PROVIDER",
        "openai",
    ).strip().lower()

    if provider == "gemini":
        return call_gemini(prompt)

    if provider == "openai":
        return call_openai(prompt)

    raise AIConfigurationError(
        f"지원하지 않는 AI_PROVIDER입니다: {provider}"
    )


def build_prompt(
    user_query: str,
    places_context: str,
) -> str:
    """
    사용자 질문과 주변 관광지 정보를 합쳐
    OpenAI에 전달할 입력을 생성한다.
    """

    cleaned_query = user_query.strip()

    if not cleaned_query:
        raise AIServiceError(
            "사용자 질문이 비어 있습니다."
        )

    return f"""
[사용자 질문]
{cleaned_query}

[현재 위치 주변 관광지 정보]
{places_context}

위 관광지 정보를 우선적으로 참고하여
사용자의 질문에 답변해 줘.
""".strip()


def call_openai(prompt: str) -> str:
    """
    OpenAI Responses API를 호출하여 답변을 생성한다.
    """

    api_key = require_environment_variable(
        "OPENAI_API_KEY"
    )

    model_name = os.getenv(
        "OPENAI_MODEL",
        "gpt-5-mini",
    ).strip()

    if not model_name:
        raise AIConfigurationError(
            "OPENAI_MODEL 환경변수를 설정해야 합니다."
        )

    try:
        from openai import OpenAI, OpenAIError

    except ImportError as exc:
        raise AIConfigurationError(
            "openai 패키지가 설치되어 있지 않습니다. "
            "'pip install openai'를 실행해 주세요."
        ) from exc

    try:
        client = OpenAI(
            api_key=api_key,
            timeout=30.0,
            max_retries=2,
        )

        response = client.responses.create(
            model=model_name,
            instructions=SYSTEM_INSTRUCTIONS,
            input=prompt,
            max_output_tokens=700,
        )

        answer = response.output_text

        if not answer or not answer.strip():
            raise AIServiceError(
                "OpenAI가 비어 있는 응답을 반환했습니다."
            )

        return answer.strip()

    except AIServiceError:
        raise

    except OpenAIError as exc:
        raise AIServiceError(
            f"OpenAI API 호출에 실패했습니다: {exc}"
        ) from exc

    except Exception as exc:
        raise AIServiceError(
            "AI 답변을 생성하는 중 예상하지 못한 "
            "오류가 발생했습니다."
        ) from exc

def call_gemini(prompt: str) -> str:
    """
    Gemini API를 호출하여 답변을 생성한다.
    """

    api_key = require_environment_variable(
        "GEMINI_API_KEY"
    )

    model_name = require_environment_variable(
        "GEMINI_MODEL"
    )

    try:
        import google.generativeai as genai

    except ImportError as exc:
        raise AIConfigurationError(
            "google-generativeai 패키지가 설치되어 있지 않습니다. "
            "'pip install google-generativeai'를 실행해 주세요."
        ) from exc

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SYSTEM_INSTRUCTIONS,
        )

        response = model.generate_content(prompt)

        answer = getattr(response, "text", None)

        if not answer or not answer.strip():
            raise AIServiceError(
                "Gemini가 비어 있는 응답을 반환했습니다."
            )

        return answer.strip()

    except AIServiceError:
        raise

    except Exception as exc:
        raise AIServiceError(
            "Gemini API 호출에 실패했습니다."
        ) from exc

def require_environment_variable(
    variable_name: str,
) -> str:
    """
    필수 환경변수가 존재하는지 확인한다.

    환경변수가 없으면 AIConfigurationError를 발생시킨다.
    """

    value = os.getenv(
        variable_name,
        "",
    ).strip()

    if not value:
        raise AIConfigurationError(
            f"{variable_name} 환경변수를 설정해야 합니다."
        )

    return value
