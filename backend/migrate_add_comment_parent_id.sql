-- 为 work_comments 表添加 parent_id 字段支持无限嵌套评论
ALTER TABLE work_comments 
ADD COLUMN parent_id BIGINT UNSIGNED NULL AFTER content,
ADD CONSTRAINT fk_work_comment_parent FOREIGN KEY (parent_id) REFERENCES work_comments(id) ON DELETE CASCADE;

-- 添加索引以优化查询性能
CREATE INDEX idx_work_comments_parent_id ON work_comments(parent_id);
