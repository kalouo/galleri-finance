
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from './type-utils';
import {  } from './type-aliases';

type Storage = {
    
};

type Methods = {
    
};

type MethodsObject = {
    
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'LoanCoreStep000Cont0StorageCode', protocol: string, code: object[] } };
export type LoanCoreStep000Cont0StorageContractType = ContractAbstractionFromContractType<contractTypes>;
export type LoanCoreStep000Cont0StorageWalletType = WalletContractAbstractionFromContractType<contractTypes>;
