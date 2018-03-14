# coding:utf-8
# 栈的实现：最基本的形式本质上就是一个列表，只不过要加一些限制
class Stack():
    def __init__(self, size): #初始化栈
        self.stack=[] #将一个列表赋给stack
        self.size=size #将栈的容量初始化为传递进来的一个数字
        self.top=-1 #定义最开始栈顶的位置为-1

    def push(self, content): #入栈函数
        if self.Full():
            print "full"
        else:
            self.stack.append(content) #用append（）方法增加数据
            self.top=self.top+1 #栈顶指针自加1

    def out(self): #出栈函数
        if self.Empty():
            print "empty"
        else:
            self.top=self.top-1
            self.stack.pop()
            
    def Full(self):
        if self.top==self.size:#如果栈顶指针等于栈的容量值，说明栈满了
            return True
        else:
            return  False

    def Empty(self):
        if self.top==-1: #当栈顶与栈底重合时说明栈为空
            return True
        else:
            return False

if __name__=="__main__":
    a = Stack(5)
    a.push("2")
    print a.stack,a.size,a.top
    a.push("1")
    a.push("3")
    print a.stack,a.size,a.top
    a.out()
    print a.stack,a.size,a.top
    
    
