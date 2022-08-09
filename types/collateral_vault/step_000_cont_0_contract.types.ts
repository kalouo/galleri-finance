
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from './type-utils';
import { address, BigMap, nat } from './type-aliases';

type Storage = {
    deposits: BigMap<nat, {
        collateral_contract: address;
        collateral_token_id: nat;
        deposit_amount: nat;
    }>;
    owner: address;
};

type Methods = {
    deposit: (
        amount: nat,
        collateral_contract: address,
        collateral_token_id: nat,
        deposit_id: nat,
        depositor: address,
    ) => Promise<void>;
    withdraw: (
        deposit_id: nat,
        recipient: address,
    ) => Promise<void>;
};

type MethodsObject = {
    deposit: (params: {
        amount: nat,
        collateral_contract: address,
        collateral_token_id: nat,
        deposit_id: nat,
        depositor: address,
    }) => Promise<void>;
    withdraw: (params: {
        deposit_id: nat,
        recipient: address,
    }) => Promise<void>;
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'CollateralVaultStep000Cont0ContractCode', protocol: string, code: object[] } };
export type CollateralVaultStep000Cont0ContractContractType = ContractAbstractionFromContractType<contractTypes>;
export type CollateralVaultStep000Cont0ContractWalletType = WalletContractAbstractionFromContractType<contractTypes>;
