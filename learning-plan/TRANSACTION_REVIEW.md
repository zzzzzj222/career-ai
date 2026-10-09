# ORM事务复习：提交、刷新、回滚

围绕现有Article + MySQL + SQLAlchemy AsyncSession学习。以下都是推演题，不要求实际写入数据库或补做已免除的HTTP验收。

## 先记住这条边界

**rollback只能撤销当前事务中尚未提交的更改，不能撤销此前成功的commit。**

| 操作 | 作用 | 是否提交事务 |
| --- | --- | --- |
| db.add(article) | 把新对象交给Session管理，通常尚未执行INSERT | 否 |
| await db.flush() | 把待处理更改发为SQL执行，可能取得数据库生成的ID | 否 |
| await db.commit() | 先flush，再提交当前事务 | 是 |
| await db.refresh(article) | 通过查询从数据库重新加载对象属性，覆盖对应内存值 | 否 |
| await db.rollback() | 撤销当前未提交事务，并调整Session中的对象状态 | 否 |

SQL已经执行、拿到了ID、在同一事务里查到了数据，都不等于事务已提交。这里假定MySQL使用支持事务的表（例如InnoDB）。回滚插入后，自增ID可能留下空号，不要求编号恢复。

## 对照现有代码

week02/day12/article_api/crud.py的_save_article先执行commit，再执行refresh。

```python
await db.commit()          # 成功返回：这个事务的更改已经提交
await db.refresh(article) # 再读数据库；如果这里失败，前面的提交仍然有效
```

所以“请求最终报错”和“数据库没有保存”并非同一件事。提交成功但响应构造失败时，仍可能已经保存。要撤销业务结果，需要另开事务UPDATE/DELETE并再次commit；这属于业务补偿，也可能失败。

refresh不是清空所有缓存，也不是提交。它重新加载某个ORM对象的数据库状态；不要把它当作保护未提交修改的操作。

## 四个场景

1. 新增A，flush成功，随后抛异常并rollback：A的插入被撤销，即使之前已经获得ID。
2. 新增A，commit成功，refresh失败，然后rollback：A仍已保存。
3. 原标题“旧”，改为“新”并commit成功；又改为“再改”并flush，再rollback：数据库保留“新”。回滚撤销第二段未提交事务。
4. 同一事务新增A和B，B在flush时报约束错误，尚未commit：rollback撤销这个事务中的更改，包括A。flush失败后须rollback才能继续正常使用Session。

## 自测（先口述，再核对上述解释）

- 为什么取得article.id不能证明数据已经提交？
- commit成功但refresh失败，此时rollback能删除刚创建的文章吗？
- 标题“旧”→“新”（commit成功）→“再改”（flush后rollback），数据库最终是哪一个？
- 一个业务要求A和B必须同时成功，为什么分别commit A和B不能保证这个要求？

完成标准：无需看笔记，能指出每个场景的commit边界，解释最终数据状态，并区分rollback与新的补偿事务。仅收到讲解或表示同意不记为掌握。

## 短期复习安排

- 本次：5–10分钟完成前三道口述题；按答复只补一个最关键误区。
- 下一次学习/22:30跟进：5分钟换成UPDATE和DELETE场景，不重复基础接口验收。
- 再隔2–3个学习日：5–10分钟解释同一事务与两个独立事务的差别；通过后降低复习频率。
- 这些练习计入每天3–4小时，不额外叠加。若仍混淆，先做30分钟最小推演，再衔接Session生命周期。

资料：[SQLAlchemy Session：Flushing、Committing、Rolling Back](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)。
