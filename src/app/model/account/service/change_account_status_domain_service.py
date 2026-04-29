from dataclasses import dataclass
from src.app.model.account.entities.principals import Account, AccountStatus
from src.app.model.account.entities.metadata import AccountMetadata


@dataclass
class ChangeStatusData:
    account: Account
    metadata: AccountMetadata
    updated_status: AccountStatus


class ChangeAccountStatusDomainService:
    @staticmethod
    def exec(change_status_data: ChangeStatusData) -> None:
        if change_status_data.updated_status == AccountStatus.ACTIVE:
            change_status_data.account.to_active()
            change_status_data.metadata.update()
            return

        elif change_status_data.updated_status == AccountStatus.SUSPENDED:
            change_status_data.account.to_suspended()
            change_status_data.metadata.update()
            return

        raise ValueError("そんな状態はないよ")
