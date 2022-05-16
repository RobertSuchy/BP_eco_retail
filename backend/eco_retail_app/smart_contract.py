from re import L
from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program


def approval():
    # global_escrow = Bytes("escrow") # byteslice
    local_user_type = Bytes("user_type") # byteslice
    # local_reward = Bytes("reward") # uint64
    global_asset_id = Bytes("asset_id")
    
    customer = Bytes("customer")
    chain_store = Bytes("chainStore")
    producer = Bytes("producer")
    op_send_reward = Bytes("send_reward")
    # op_set_escrow = Bytes("set_escrow")
    op_create_asa = Bytes("create_asa")
    op_exchange_asa = Bytes("exchange_asa")
    # op_c2c = Bytes("c2c")


    @Subroutine(TealType.none)
    def opt_in(account: Expr):
        return App.localPut(account, local_user_type, Txn.application_args[0])


    @Subroutine(TealType.none)
    def create_asa():
        return Seq(
            Assert(Txn.sender() == Global.creator_address()),
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_total: Int(1000000),
                TxnField.config_asset_decimals: Int(0),
                TxnField.config_asset_unit_name: Bytes("ERC"),
                TxnField.config_asset_name: Bytes("EcoRetail Coin"),
                TxnField.config_asset_manager: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_clawback: Global.current_application_address()
            }),
            InnerTxnBuilder.Submit(),
            App.globalPut(global_asset_id, InnerTxn.created_asset_id()), 
            # Log(InnerTxn.created_asset_id()),
            Approve()
        )


    @Subroutine(TealType.none)
    def exchange_asa():
        return Seq(
            program.check_self(group_size=Int(2), group_index=Int(0)),
            program.check_rekey_zero(2),
            Assert(
                And(
                    Gtxn[1].type_enum() == TxnType.Payment,
                    App.localGet(Int(0), local_user_type) == chain_store
                )
            ),
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_amount: Btoi(Txn.application_args[1]),
                TxnField.xfer_asset: App.globalGet(global_asset_id)
            }),
            InnerTxnBuilder.Submit(),
            Approve()
        )


    @Subroutine(TealType.none)
    def send_reward(account: Expr):
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_amount: Btoi(Txn.application_args[1]),
                TxnField.xfer_asset: Int(20)
            }),
            InnerTxnBuilder.Submit(),
            Approve()
        )


    # @Subroutine(TealType.none)
    # def init(account: Expr):
    #     return Seq(
    #         App.localPut(account, local_customer, Txn.application_args[0]),
    #         App.localPut(account, local_reward, Btoi(Txn.application_args[1]))
    #     )


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


    # @Subroutine(TealType.none)
    # def set_escrow():
    #     return Seq([
    #         Assert(Txn.sender() == Global.creator_address()),
    #         App.globalPut(global_escrow, Txn.application_args[1]),
    #         Approve()
    #     ])


    # @Subroutine(TealType.none)
    # def create_asa():
    #     return Seq([
    #         Assert(Global.group_size() == Int(2)),
    #         Assert(Gtxn[1].sender() == App.globalGet(global_escrow)),
    #         Assert(
    #             And(
    #                 Gtxn[1].type_enum() == TxnType.AssetConfig,
    #                 Eq(Gtxn[1].config_asset_name(), Bytes("EcoRetail Coin")),
    #             )
    #         ),
    #         Approve()
    #     ])

    return program.event(
        init = Approve(),
        delete = Approve(),
        update=Approve(),
        opt_in = Seq( 
            opt_in(Int(0)),
            Approve()
        ),
        no_op = Seq(
            Cond(
                [Txn.application_args[0] == op_send_reward, send_reward(Int(0))],
                [Txn.application_args[0] == op_create_asa, create_asa()],
                [Txn.application_args[0] == op_exchange_asa, exchange_asa()],
                # [Txn.application_args[0] == op_set_escrow, set_escrow()],
                # [Txn.application_args[0] == op_c2c, c2c()],
            ),
            Reject()
        )
    )

def clear():
    return Approve()
