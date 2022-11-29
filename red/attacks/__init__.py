import enum


class Attack(str, enum.Enum):
    apache_push_diary = 'apache-push-diary'

    def get_script(self):
        if self == "apache-push-diary":
            from . import apache_push_diary
            return apache_push_diary
