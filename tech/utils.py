import random
import string

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


print(random_string_generator())

print(random_string_generator(size=50))

def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.slug = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range())
            super().save(*args, **kwargs)
        except IntegrityError:
            self.save(*args, **kwargs)