// gcc -c mylib.c && gcc -shared -o libmylib.so mylib.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char name[255];
} Person;

extern Person *person_create(char *);
extern void    person_greet(Person *person);
extern void    person_free(Person *person);

Person *person_create(char *name) {
    Person *p = malloc(sizeof(Person));
    strcpy(p->name, name);
    return p;
}

void person_greet(Person *person) {
    printf("Hi, my name is %s\n", person->name);
}

void person_free(Person *person) {
    free(person);
}