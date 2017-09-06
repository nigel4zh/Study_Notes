
### class()
+ **用途**：查看变量的类
+ **用法**：class(var)

### c()
+ **用途**：创建向量
+ **用法**：c("str1", "str2", "str3")

### names()
+ **用途**：给变量（中的每个元素）命名
+ **用法**：names(vec) <- c("str1", "str2", "str3") 或者 names(vec) <- var

### sum()
+ **用途**：计算向量（中的所有元素）的和
+ **用法**：sum(vec)

### vec[ ]
+ **用途**：选取向量中的部分
+ **用法**：vec[c(1,2,3)]，vec[1:3]，vec["ele_names"]，vec[c("ele_names1","ele_names2","ele_names3")]，vec[var]

### mean()
+ **用途**：计算向量（中的所有元素）的平均数
+ **用法**：mean(vec)

### matrix()
+ **用途**：创建矩阵
+ **用法**：matrix(1:9, byrow = TRUE, nrow = 3, dimnames = list(c("str1", "str2"),c("stra", "strb")))

    > `1:9`  代表向量，即需要填充元素的集合

    > `byrow = TRUE`  代表按行填充

    > `nrow = 3`  代表矩阵有3行

    > `dimnames = list()`  代表给数据的每一个维度命名，矩阵是二维数组
    

### rownames(), colnames()
+ **用途**：给矩阵的行、列命名
+ **用法**：row/colnames(vec) <- c("str1", "str2", "str3") 或者 row/colnames(vec) <- var

### rowSums(), colSums()
+ **用途**：对行，列求和
+ **用法**：rowSums(mat),colSums(mat)

### cbind(), rbind()
+ **用途**：对矩阵和向量从列、行的角度合并
+ **用法**：cbind/rbind(ob1. ob2)

### factor()
+ **用途**：将向量转为factor，即向量中不重复的元素集合
+ **用法**：factor(var, order = TRUE, levels = c("str1", "str2", "str3"))

    > `levels和labels`  levels用来指定factor可能的水平（默认是向量var中互异的值）；labels用来指定levels的名字

    > `order = TRUE`  指示factor有序，并且以参数`levels`指定为序

### summary()
+ **用途**：获取变量的描述性统计量
+ **用法**：summary(var)

### head(), tail()
+ **用途**：获取数据框的前六行、后六行
+ **用法**：head(df), tail(df)

### str()
+ **用途**：获取数据集的结构

    > 对于数据框来说，包括总观察行数，总变量数，变量名列表，每个变量的数据类型，以及第一行

+ **用法**：str(ds)

### data.frame()
+ **用途**：创建数据框
+ **用法**：data.frame(vec)

### df$var_nm
+ **用途**：选择数据框中某一个变量下的所有数据
+ **用法**：data_frame$variable_name

### subset()
+ **用途**：指定数据框的子集
+ **用法**：subset(df, 筛选条件)

### order(var)
+ **用途**：给出var中每个元素的排序位置（这里的排序类似于Excel里的排序）
+ **用法**：order(var)

### df[筛选条件,]
+ **用途**：数据框的切片/选择
+ **用法**：筛选条件如果设置为`order`后的变量，即可对整个数据框进行排序

### list()
+ **用途**：创建列表
+ **用法**：list(obj1, obj2, obj3), 可以存储不同类型的变量（向量、矩阵、数据框）