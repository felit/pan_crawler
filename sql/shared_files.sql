CREATE TABLE shared_files (
  id int(8) PRIMARY KEY AUTO_INCREMENT,
  shorturl        VARCHAR(32) COMMENT '共享短URL',
  like_count      INT(2),
  dCnt            INT(2),
  category        INT(6) COMMENT '类别',
  title           text COMMENT 'title',
  comment_count   INT(4),
  feed_time       DATETIME,
  public          INT(2),
  username        VARCHAR(32) COMMENT '用户名称',
  source_uid      VARCHAR(32) COMMENT '',
  like_status     INT(2),
  feed_type       VARCHAR(32),
  vCnt            VARCHAR(16),
  filecount       INT(4) COMMENT '文件数',
  description     VARCHAR(128) COMMENT '文件描述',
  third           INT(2),
  data_id         VARCHAR(32),
  tCnt            INT(4),
  clienttype      INT(4),
  isdir           INT(2),
  server_filename VARCHAR(256) COMMENT '服务器文件名称',
  path            TEXT COMMENT '路径',
  size            INT(8) COMMENT '文件大小(Byte)',
  avatar_url      VARCHAR(256) COMMENT '头像URL',
  shareid         VARCHAR(128) COMMENT '共享编号',
  uk              varchar(32) COMMENT '帐号编号',
  source_id       varchar(32)
)
  ENGINE =InnoDB
  AUTO_INCREMENT =32
  DEFAULT CHARSET =utf8
  COMMENT '共享文件信息';
ALTER TABLE shared_files ADD INDEX index_uk(uk);
ALTER TABLE shared_files ADD INDEX index_shorturl(shorturl);