-- 个人资料编辑功能 - 数据库迁移脚本
-- 执行时间：2026-05-08
-- 说明：为 users 表添加新字段以支持个人资料编辑功能

-- 1. 添加 bio 字段（个性签名，最多150字）
ALTER TABLE `users` 
ADD COLUMN `bio` TEXT NULL COMMENT '个性签名（最多150字）' AFTER `signature`;

-- 2. 添加 is_real_name_public 字段（是否公开姓名）
ALTER TABLE `users` 
ADD COLUMN `is_real_name_public` SMALLINT DEFAULT 0 COMMENT '是否公开真实姓名（0=否，1=是）' AFTER `major`;

-- 3. 添加 is_major_public 字段（是否公开专业）
ALTER TABLE `users` 
ADD COLUMN `is_major_public` SMALLINT DEFAULT 0 COMMENT '是否公开专业/学院（0=否，1=是）' AFTER `is_real_name_public`;

-- 4. 为现有用户设置默认值（nickname 初始设为 account）
UPDATE `users` 
SET `bio` = `signature` 
WHERE `bio` IS NULL AND `signature` IS NOT NULL;

-- 验证修改
SELECT 
    id,
    account,
    nickname,
    bio,
    real_name,
    major,
    is_real_name_public,
    is_major_public
FROM `users`
LIMIT 5;
