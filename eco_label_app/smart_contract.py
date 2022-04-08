from re import L
from pyteal import *
from pyteal.ast.bytes import Bytes
from .pyteal_helpers import program


def approval():
    global_escrow = Bytes("escrow") # byteslice
    # local_customer = Bytes("customer") # byteslice
    # local_reward = Bytes("reward") # uint64
    
    # op_add = Bytes("add")
    op_send_reward = Bytes("send_reward")
    op_set_escrow = Bytes("set_escrow")
    op_create_asa = Bytes("create_asa")
    # op_c2c = Bytes("c2c")

    # @Subroutine(TealType.none)
    # def init(account: Expr):
    #     return Seq(
    #         App.localPut(account, local_customer, Txn.application_args[0]),
    #         App.localPut(account, local_reward, Btoi(Txn.application_args[1]))
    #     )

    # @Subroutine(TealType.none)
    # def add(account: Expr):
    #     return Seq(






    #         Approve()
    #     )

    @Subroutine(TealType.none)
    def send_reward(account: Expr):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.Payment,
                    TxnField.receiver: Txn.application_args[1],
                    # TxnField.amount: Int(1000),
                    TxnField.amount: Btoi(Txn.application_args[2]),
                    TxnField.fee: Int(0)
                }
            ),
            InnerTxnBuilder.Submit(),
            Approve()
        )

    @Subroutine(TealType.none)
    def set_escrow():
        return Seq([
            Assert(Txn.sender() == Global.creator_address()),
            App.globalPut(global_escrow, Txn.application_args[1]),
            Approve()
        ])

    @Subroutine(TealType.none)
    def create_asa():
        return Seq([
            Assert(Global.group_size() == Int(2)),
            Assert(Gtxn[1].sender() == App.globalGet(global_escrow)),
            Assert(
                And(
                    Gtxn[1].type_enum() == TxnType.AssetConfig,
                    Eq(Gtxn[1].config_asset_name(), Bytes("EcoLabel Coin")),
                )
            ),
            Approve()
        ])

    # @Subroutine(TealType.none)
    # def c2c():
    #     app_id = Btoi(Txn.application_args[1])

    #     return Seq(
    #         InnerTxnBuilder.Begin(),
    #         InnerTxnBuilder.SetFields(
    #             {
    #                 TxnField.type_enum: TxnType.ApplicationCall,
    #                 TxnField.application_id: Txn.applications[app_id],
    #                 TxnField.application_args: [Bytes("send")],
    #                 TxnField.fee: Int(0)
    #             }
    #         ),
    #         InnerTxnBuilder.Submit(),
    #         Approve()
    #     )

    return program.event(
        init = Approve(),
        opt_in = Seq( 
            # init(Int(0)),
            Approve()
        ),
        no_op = Seq(
            Cond(
                # [Txn.application_args[0] == op_add, add(Int(0))],
                [Txn.application_args[0] == op_send_reward, send_reward(Int(0))],
                [Txn.application_args[0] == op_set_escrow, set_escrow()],
                [Txn.application_args[0] == op_create_asa, create_asa()]
                # [Txn.application_args[0] == op_c2c, c2c()],
            ),
            Reject()
        )
    )

def clear():
    return Approve()
