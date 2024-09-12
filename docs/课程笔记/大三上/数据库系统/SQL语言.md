## 语言概述

### SQL概览

1974，由Boyce与Chamber提出，是集DDl，DML，DCL于一体的数据库语言

1. DDL语句引导词：`CREATE`，`ALTER`，`DROP`
2. DML语句引导词：`INSERT`，`UPDATE`，`DELETE`，`SELECT`
3. DCL语句引导词：`GRANT`，`REVOKE`

## 简单的SQL-DDl/DML：创建数据库

### 创建数据库

```sql
CREATE DATABASE <dbname>;
```

### 创建表

```sql
CREATE TABLE <tbname> (<col_name data_type [PRIMARY KEY | UNIQUE] [NOT NULL] [, col_name_data_type]>, ...);
```

- `[ ]`：表示内部内容可以省略<br>
- `|`：表示隔开选项可以任选其一<br>
- `UNIQUE`：唯一性约束，即候选键<br>
- `NOT NULL`：指该列不允许出现空值，通常主键是不允许有空值

> 各个商用DBMS的数据类型或有差异

例：

```sql
CREATE TABLE COURSE(CNo char(3), CName char(12))
```

### 向表中追加元组 `INSERT INTO`

```sql
INSERT INTO <tbname> (<colname>[,<colname>]) VALUES (<val>[, <val>], ...);
```

## SQL-DML之查询SELECT

### 基本检索操作

```sql
SELECT <colname> 
FROM <tbname>  
 |WHERE <conditions>;
```

例：

```sql
SELECT SNo, Sname, Sage FROM Students WHERE Sage <= 19;
```

### 子查询

### 分组查询

### 空值处理

### SQL的完整语法

## SQL-DML之更新INSERT/UPDATE/DELETE

## SQL-视图及DDL的进一步介绍