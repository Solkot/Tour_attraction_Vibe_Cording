CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 게시글 고유 번호 (자동 증가)
    title TEXT NOT NULL,                  -- 게시글 제목
    content TEXT NOT NULL,                -- 게시글 본문
    category TEXT NOT NULL,               -- 카테고리 (예: '관광지', '맛집', '숙소')
    password TEXT NOT NULL,               -- 수정/삭제용 비밀번호 (RFP 요구사항에 따라 평문 저장)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- 작성 시간 (기본값 현재 시간)
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- 수정 시간
);