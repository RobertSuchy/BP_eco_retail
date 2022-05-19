from re import L
from pyteal import *
from pyteal.ast.bytes import Bytes
from pyteal_helpers import program


def approval():
    local_user_type = Bytes("user_type") # byteslice
    global_asset_id = Bytes("asset_id") # uint64
    
    customer = Bytes("customer")
    chain_store = Bytes("chainStore")
    producer = Bytes("producer")
    op_send_reward = Bytes("send_reward")
    op_create_asa = Bytes("create_asa")
    op_exchange_asa = Bytes("exchange_asa")
    op_add_product = Bytes("add_product")


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
                    App.optedIn(Int(0), Int(0)),
                    App.localGet(Int(0), local_user_type) == chain_store,
                    Gtxn[1].receiver() == Global.current_application_address(),
                    Txn.application_args.length() == Int(2),
                    Btoi(Txn.application_args[1]) * Int(10_000) == Gtxn[1].amount()
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
    def add_product():
        return Seq(
            Assert(App.localGet(Int(0), local_user_type) == producer),
            Approve()
        )


    @Subroutine(TealType.none)
    def send_reward():
        return Seq(
            program.check_self(group_size=Int(2), group_index=Int(0)),
            program.check_rekey_zero(2),
            Assert(
                And(
                    Gtxn[1].type_enum() == TxnType.AssetTransfer,
                    App.optedIn(Int(0), Int(0)),
                    App.optedIn(Int(1), Int(0)),
                    App.localGet(Int(0), local_user_type) == chain_store,
                    App.localGet(Int(1), local_user_type) == customer,
                    Txn.sender() == Gtxn[1].sender(),
                    # Txn.accounts[1] == Gtxn[1].receiver(),
                    Txn.application_args.length() == Int(2),
                    App.globalGet(global_asset_id) == Gtxn[1].xfer_asset(),
                    Btoi(Txn.application_args[1]) == Gtxn[1].asset_amount()
                )
            ),
            Approve()
        )


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
                [Txn.application_args[0] == op_create_asa, create_asa()],
                [Txn.application_args[0] == op_exchange_asa, exchange_asa()],
                [Txn.application_args[0] == op_add_product, add_product()],
                [Txn.application_args[0] == op_send_reward, send_reward()]
            ),
            Reject()
        )
    )


def clear():
    return Approve()
