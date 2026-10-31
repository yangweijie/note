---
title: "Git回滚代码到某个commit"
date: 2020-03-26
tags: []
summary: "Git回滚代码到某个commit"
---

Git回滚代码到某个commit
回退命令：

$ git reset --hard HEAD^ 回退到上个版本
$ git reset --hard HEAD~3 回退到前3次提交之前，以此类推，回退到n次提交之前
$ git reset --hard commit_id 退到/进到 指定commit的sha码

强推到远程：

$ git push origin HEAD --force
