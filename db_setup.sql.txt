-- ========== 建库 ==========
CREATE DATABASE video_mgmt;
GO
USE video_mgmt;
GO

-- ========== 建表 ==========
CREATE TABLE [user] (
    user_id INT IDENTITY(1,1) PRIMARY KEY, 
    username NVARCHAR(50) NOT NULL UNIQUE,
    role NVARCHAR(20) DEFAULT 'student' CHECK (role IN ('student', 'teacher', 'admin')), 
    created_at DATETIME DEFAULT GETDATE()
);
GO

CREATE TABLE video (
    video_id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(200) NOT NULL,
    description NVARCHAR(MAX), 
    file_path NVARCHAR(500) NOT NULL, 
    duration INT NOT NULL, 
    uploader_id INT NOT NULL,
    upload_time DATETIME DEFAULT GETDATE(),
    CONSTRAINT fk_video_uploader FOREIGN KEY (uploader_id) REFERENCES [user](user_id) ON DELETE CASCADE
);
GO

CREATE TABLE tag (
    tag_id INT IDENTITY(1,1) PRIMARY KEY,
    tag_name NVARCHAR(50) NOT NULL UNIQUE
);
GO

CREATE TABLE video_tag (
    video_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (video_id, tag_id),
    CONSTRAINT fk_vt_video FOREIGN KEY (video_id) REFERENCES video(video_id) ON DELETE CASCADE,
    CONSTRAINT fk_vt_tag FOREIGN KEY (tag_id) REFERENCES tag(tag_id) ON DELETE CASCADE
);
GO

-- ========== 建索引 ==========
CREATE NONCLUSTERED INDEX idx_video_upload_time ON video(upload_time DESC);
CREATE NONCLUSTERED INDEX idx_video_tag_tagid ON video_tag(tag_id);
GO

-- ========== 建视图 ==========
CREATE VIEW v_video_detail AS
SELECT 
    v.video_id, v.title AS 视频标题, v.duration AS 时长, u.username AS 上传者,
    STUFF((SELECT ', ' + t2.tag_name FROM video_tag vt2 JOIN tag t2 ON vt2.tag_id = t2.tag_id WHERE vt2.video_id = v.video_id FOR XML PATH('')), 1, 2, '') AS 标签列表
FROM video v
JOIN [user] u ON v.uploader_id = u.user_id;
GO

-- ========== 建存储过程 ==========
CREATE PROCEDURE sp_add_video
    @title NVARCHAR(200), @file_path NVARCHAR(500), @duration INT, @uploader_id INT, @tag_id INT
AS
BEGIN
    BEGIN TRANSACTION;
    BEGIN TRY
        INSERT INTO video (title, file_path, duration, uploader_id) VALUES (@title, @file_path, @duration, @uploader_id);
        DECLARE @new_video_id INT;
        SET @new_video_id = SCOPE_IDENTITY();
        INSERT INTO video_tag (video_id, tag_id) VALUES (@new_video_id, @tag_id);
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
    END CATCH
END;
GO