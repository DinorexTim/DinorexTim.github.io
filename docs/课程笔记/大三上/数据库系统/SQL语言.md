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

#### IN谓词

练习：求选修了001号课程的学生的学号和姓名

```sql
SELECT sno, sname FROM Student
WHERE sno IN (
    SELECT sno FROM SC WHERE cno == "001"
);
```

- 求既学过001号课程，又学过002号课程学生的学号

```sql
SELECT sno FROM SC
WHERE cno = "001" AND sno IN(SELECT sno FROM SC WHERE cno = "002");
```

- 列出**没有**学过李明老师讲授课程的所有同学的姓名

```sql
SELECT sname FROM Student
WHERE sno NOT IN(
    SELECT sno FROM SC ,Course C, Teacher T
    WHERE T.name = "李明"
    AND SC.cno = C.cno
    AND T.tno = C.tno
);
```

#### 相关子查询

内层查询有时候需要依靠外层查询的某些参量作为**限定条件**才能进行

外层向内层传递的参量需要使用**外层的表名或者表别名来限定**

例：求学过001号课程同学的姓名

```sql
SELECT sname
FROM Student Stud
WHERE sno IN(
    SELECT sno 
    FROM SC 
    WHERE sno = Stud.sno AND cno = "001"
);
```

#### $\theta$ SOME/ $\theta$ ALL谓词

例：找出**工资最低**的教师姓名

```sql
SELECT tname FROM Teacher
WHERE salary <= ALL(SELECT salary FROM Teacher);
```

例：找出所有课程**都不及格**的学生姓名

```sql
SELECT sname FROM Student
WHERE 60 > ALL(SELECT score FROM SC WHERE sno = Studnet.sno);
```

#### EXISTS谓词

基本语法：`[NOT] EXISTS (子查询)`

例：检索选修了李明老师主讲课程的**所有同学**的姓名

```sql
SELECT DISTINCT sname FROM Student
WHERE EXISTS (
    SELECT * FROM SC, Course, Teacher 
    WHERE SC.cno = Course.cno 
        AND SC.sno = Student.sno 
        AND Course.tno = Teacher.tno 
        AND tname = "李明");
```

Extra: 强大的`NOT EXISTS`

例：检索学过001号老师主讲的所有课程的所有同学的姓名

> 可以将其转化为“**不存在**有一门001号老师主讲的课程该同学**没学过**”<br>
> 本质是全称量词$\forall$与存在量词$\exists$的转换

```sql
SELECT DISTINCT sname FROM Student  
WHERE NOT EXISTS(   -- 不存在
    SELECT * FROM Course    -- 有一门001教师主讲课程
    WHERE Course.tno = "001" AND NOT EXISTS(    -- 该同学没学过
        SELECT * FROM SC 
        WHERE sno = Student.sno AND cno = Course.cno
    )
)
```

### 分组查询

### 空值处理

### SQL的完整语法

## SQL-DML之更新INSERT/UPDATE/DELETE

## SQL-视图及DDL的进一步介绍