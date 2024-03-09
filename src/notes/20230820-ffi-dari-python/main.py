import cffi


ffi = cffi.FFI()

ffi.cdef(
    """
    typedef struct {
        char name[255];
    } Person;

    Person* person_create(char*);
    void person_greet(Person *person);
    void person_free(Person *person);
    """
)

lib = ffi.dlopen("libmylib.so")


class Person:
    def __init__(self, name: str) -> None:
        self.person_ = lib.person_create(bytes(name, "utf-8"))

    def __del__(self) -> None:
        lib.person_free(self.person_)

    def greet(self) -> None:
        lib.person_greet(self.person_)

    @property
    def name(self) -> str:
        return ffi.string(self.person_.name).decode()


john = Person("John")
john.greet()
print(john.name)
