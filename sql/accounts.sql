CREATE TABLE accounts (
  id int(8) PRIMARY KEY AUTO_INCREMENT,
  follow_uk         varchar(32),
  fans_count        INT(4) COMMENT '粉丝数',
  parent_follow_uk  TEXT COMMENT '关注帐号的follow_uk',
  avatar_url        TEXT COMMENT '头像URL',
  pubshare_count    INT(4) COMMENT '公享文件数',
  follow_uname      VARCHAR(128) COMMENT '名称',
  follow_count      INT(4) COMMENT '关注帐号数',
  user_type         INT(2),
  intro             text COMMENT '帐号简介',
  album_count       INT(2),
  is_vip            INT(2) COMMENT '是否是VIP',
  type              INT(2),
  follow_time       DATETIME,
  create_time       DATETIME COMMENT '创建时间',
  update_time       DATETIME COMMENT '最后更新时间',
  is_follow_crawler BOOLEAN COMMENT '是否已经抓取',
  is_files_crawler  BOOLEAN COMMENT '文件是否已经抓取'
)
  ENGINE =InnoDB
  AUTO_INCREMENT =32
  DEFAULT CHARSET =utf8
  COMMENT '帐号信息';

ALTER TABLE accounts ADD INDEX index_follow_uk(follow_uk);
ALTER TABLE accounts ADD INDEX index_pubshare_count(pubshare_count);
ALTER TABLE accounts ADD INDEX index_create_time(create_time);