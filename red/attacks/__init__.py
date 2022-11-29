import enum


class Attack(str, enum.Enum):
    apache_push_diary = 'apache-push-diary'
    check_default_credentials = 'check-default-credentials'
    concurrent_ids = 'concurrent-ids'
    create_users = 'create-users'
    inject_money = 'inject-money'
    too_much_money = 'too-much-money'
    withdraw_all = 'withdraw-all'
    withdraw_all_from_default = 'withdraw-all-from-default'

    def get_script(self):
        if self == self.apache_push_diary:
            from . import apache_push_diary
            return apache_push_diary
        elif self == self.check_default_credentials:
            from . import check_default_credentials
            return check_default_credentials
        elif self == self.concurrent_ids:
            from . import concurrent_ids
            return concurrent_ids
        elif self == self.create_users:
            from . import create_users
            return create_users
        elif self == self.inject_money:
            from . import inject_money
            return inject_money
        elif self == self.too_much_money:
            from . import too_much_money
            return too_much_money
        elif self == self.withdraw_all:
            from . import withdraw_all
            return withdraw_all
        elif self == self.withdraw_all_from_default:
            from . import withdraw_all_from_default
            return withdraw_all_from_default
