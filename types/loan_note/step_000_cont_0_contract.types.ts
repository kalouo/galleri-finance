
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from './type-utils';
import { address, BigMap, bytes, contract, MMap, nat, unit } from './type-aliases';

type Storage = {
    administrator: address;
    last_token_id: nat;
    ledger: BigMap<nat, address>;
    metadata: BigMap<string, bytes>;
    operators: BigMap<{
        owner: address;
        operator: address;
        token_id: nat;
    }, unit>;
    token_metadata: BigMap<nat, {
        token_id: nat;
        token_info: MMap<string, bytes>;
    }>;
};

type Methods = {
    balance_of: (
        requests: Array<{
            owner: address;
            token_id: nat;
        }>,
        callback: contract,
    ) => Promise<void>;
    burn: (param: nat) => Promise<void>;
    mint: (param: Array<{
            token_id: nat;
            to: address;
            metadata: MMap<string, bytes>;
        }>) => Promise<void>;
    set_administrator: (param: address) => Promise<void>;
    transfer: (param: Array<{
            from_: address;
            txs: Array<{
                to_: address;
                token_id: nat;
                amount: nat;
            }>;
        }>) => Promise<void>;
    add_operator: (
        owner: address,
        operator: address,
        token_id: nat,
    ) => Promise<void>;
    remove_operator: (
        owner: address,
        operator: address,
        token_id: nat,
    ) => Promise<void>;
};

type MethodsObject = {
    balance_of: (params: {
        requests: Array<{
            owner: address;
            token_id: nat;
        }>,
        callback: contract,
    }) => Promise<void>;
    burn: (param: nat) => Promise<void>;
    mint: (param: Array<{
            token_id: nat;
            to: address;
            metadata: MMap<string, bytes>;
        }>) => Promise<void>;
    set_administrator: (param: address) => Promise<void>;
    transfer: (param: Array<{
            from_: address;
            txs: Array<{
                to_: address;
                token_id: nat;
                amount: nat;
            }>;
        }>) => Promise<void>;
    add_operator: (params: {
        owner: address,
        operator: address,
        token_id: nat,
    }) => Promise<void>;
    remove_operator: (params: {
        owner: address,
        operator: address,
        token_id: nat,
    }) => Promise<void>;
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'LoanNoteStep000Cont0ContractCode', protocol: string, code: object[] } };
export type LoanNoteStep000Cont0ContractContractType = ContractAbstractionFromContractType<contractTypes>;
export type LoanNoteStep000Cont0ContractWalletType = WalletContractAbstractionFromContractType<contractTypes>;
