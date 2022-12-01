import enum


class Attack(str, enum.Enum):
    all = "all"
    apache_push_diary = 'apache-push-diary'
    check_default_credentials = 'check-default-credentials'
    concurrent_ids = 'concurrent-ids'
    create_users = 'create-users'
    do_you_transact = 'do-you-transact'
    gigi_is_ok = 'gigi-is-ok'
    inject_money = 'inject-money'
    keep_very_alive = 'keep-very-alive'
    naughty = 'naughty'
    put_some = 'put-some'
    too_much_money = 'too-much-money'
    weird_names = 'weird-names'
    what_she_said = 'what-she-said'
    withdraw_all = 'withdraw-all'
    withdraw_all_from_default = 'withdraw-all-from-default'

    def get_script(self):
        if self == self.all:
            from . import all
            return all
        elif self == self.apache_push_diary:
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
        elif self == self.do_you_transact:
            from . import do_you_transact
            return do_you_transact
        elif self == self.gigi_is_ok:
            from . import gigi_is_ok
            return gigi_is_ok
        elif self == self.inject_money:
            from . import inject_money
            return inject_money
        elif self == self.keep_very_alive:
            from . import keep_very_alive
            return keep_very_alive
        elif self == self.naughty:
            from . import naughty
            return naughty
        elif self == self.put_some:
            from . import put_some
            return put_some
        elif self == self.too_much_money:
            from . import too_much_money
            return too_much_money
        elif self == self.weird_names:
            from . import weird_names
            return weird_names
        elif self == self.what_she_said:
            from . import what_she_said
            return what_she_said
        elif self == self.withdraw_all:
            from . import withdraw_all
            return withdraw_all
        elif self == self.withdraw_all_from_default:
            from . import withdraw_all_from_default
            return withdraw_all_from_default
