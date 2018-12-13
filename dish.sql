-- drop database if exists `dish`;
-- create database `dish` character set utf8mb4;
-- use `dish`;
-- set default_storage_engine=InnoDB;

drop table if exists youdao_dict;
create table youdao_dict (
	id varchar(8) not null 					              comment '文章id',
	title varchar(128) not null 				          comment '文章标题',
	url varchar(256) not null                     comment '文章url',
	`type` varchar(8) not null default ''         comment '专栏名称',
	summary varchar(1024) not null default ''     comment '摘要',
	media varchar(16) not null                    comment '媒体类型',
	keywords json                                 comment '关键词',
	style varchar(16)                             comment '风格',
	channel_id tinyint(1)                         comment '频道id',
	channel_name varchar(4)                       comment '频道名称',
  audiourl varchar(256)                         comment '音频url',
  videourl varchar(256)                         comment '视频url',
  gif json                                      comment '封面图片,',
  image json                                    comment '封面图片',
  start_time char(12)                           comment '发布时间',
  UNIQUE KEY `uk_id` (`id`) USING BTREE
) comment '有道词典上的文章';