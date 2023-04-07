package main

/*

// Our rust library output after "cargo build" will be in ./target/release.
// The "-lmylib" follows "libmylib.{so, dylib}" name.
#cgo LDFLAGS: -L./target/release -lmylib

void* new_vec2d(int x, int y);
void* vec2d_add(void* v1, void* v2);
char* vec2d_to_cstring(void* v);
int add(int a, int b);

*/
import "C"
import (
	"fmt"
	"unsafe"
)

type Vec2 struct {
	// storing pointer to rust's actual Vec2d struct
	data unsafe.Pointer
}

func NewVec2D(x int, y int) Vec2 {
	return Vec2{
		data: C.new_vec2d(C.int(x), C.int(y)),
	}
}

func (v Vec2) Add(other Vec2) Vec2 {
	newData := C.vec2d_add(v.data, other.data)
	return Vec2{data: newData}
}

func (v Vec2) String() string {
	return C.GoString(C.vec2d_to_cstring(v.data))
}

func main() {
	result := C.add(C.int(2), C.int(3))
	fmt.Println(result)

	// Raw way
	v1 := C.new_vec2d(2, 3)
	fmt.Println(C.GoString(C.vec2d_to_cstring(v1)))

	// Wrapper a "more Go" way
	v2 := NewVec2D(5, 6)
	fmt.Println(v2)

	a := NewVec2D(1, 2)
	b := NewVec2D(3, 4)
	fmt.Println(a.Add(b))
}
