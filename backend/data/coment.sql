CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,             -- 외래키 (어느 게시글의 댓글인지)
    author TEXT NOT NULL,                 -- 익명 작성자 닉네임
    content TEXT NOT NULL,                -- 댓글 내용
    password TEXT NOT NULL,               -- 수정/삭제용 비밀번호 (평문 저장)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
);