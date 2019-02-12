class Pastry:
    def accept(visitor: PastryVisitor):
        pass

class Beignet(Pastry):
    def accept(visitor: PastryVisitor):
        visitor.visitBeignet(self)


class Cruller(Pastry):
    def accept(visitor: PastryVisitor):
        visitor.visitCruller(self)


class PastryVisitor:
    def visitBeignet(self, beignet: Beignet):
        pass

    def visitCruller(self, cruller: Cruller):
        pass

# 在设计模式中通常将所有的方法都写成 visit()，通过运行时的多态性来自动调用对应的访问者方法
# 例如 Beignet#accept() 接受 PastryVisitor 实例后，会调用 visitor.visitor()，这时通过不同的 visit() 接受不同类型的参数来确定调用哪一个 visit()
