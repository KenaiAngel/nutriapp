from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')

plain = "1234"
hashed = bcrypt_context.hash(plain)
print("Hashed:", hashed)

# Verificación
print("Verify:", bcrypt_context.verify(plain, hashed))
