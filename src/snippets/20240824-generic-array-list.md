# Generic array list

```C
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define HSZ        (2 * sizeof(size_t))
#define arr_cap(a) ((size_t *)(a))[-2]
#define arr_len(a) ((size_t *)(a))[-1]
#define arr_free(a)                                                            \
    do {                                                                       \
        if (a) {                                                               \
            if (sizeof(*(a)) == sizeof(char *))                                \
                for (size_t i = 0; i < arr_len(a); i++)                        \
                    free((a)[i]);                                              \
            free((size_t *)(a)-2);                                             \
            (a) = NULL;                                                        \
        }                                                                      \
    } while (0)
#define arr_push(a, v)                                                         \
    do {                                                                       \
        if (!(a)) {                                                            \
            size_t *h = malloc(HSZ + 4 * sizeof(*(a)));                        \
            *h        = 4;                                                     \
            h[1]      = 0;                                                     \
            (a)       = (void *)(h + 2);                                       \
        }                                                                      \
        if (arr_len(a) == arr_cap(a)) {                                        \
            size_t c   = arr_cap(a) ? arr_cap(a) * 2 : 4,                      \
                   *h  = realloc((size_t *)(a)-2, HSZ + c * sizeof(*(a)));     \
            (a)        = (void *)(h + 2);                                      \
            arr_cap(a) = c;                                                    \
        }                                                                      \
        (a)[arr_len(a)] = sizeof(*(a)) == sizeof(char *) ? strdup(v) : (v);    \
        arr_len(a)++;                                                          \
    } while (0)


int main() {
    int *arr = NULL;
    arr_push(arr, 1);
    arr_push(arr, 2);
    arr_push(arr, 3);
    arr_push(arr, 4);

    printf("%d\n", arr[0]);
    arr_free(arr);

    return 0;
}
```

## Notes

- Probably will only work well with primitive types
