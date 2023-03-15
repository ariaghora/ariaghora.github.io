use std::{borrow::Borrow, ffi::CString, fmt::Display, os::raw::c_char};

pub struct Vec2d {
    x: i32,
    y: i32,
}

impl Display for Vec2d {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Vec2(x: {}, y: {})", self.x, self.y)
    }
}

#[no_mangle]
pub extern "C" fn new_vec2d(x: i32, y: i32)->*mut Vec2d {
    let v = Vec2d{x, y};
    Box::into_raw(Box::new(v))
}

#[no_mangle]
pub extern "C" fn vec2d_to_cstring(v: *mut Vec2d) -> *const c_char {
    let v = unsafe { &*(&*v).borrow() };
    let str = v.to_string();
    CString::new(str).unwrap().into_raw()
}

#[no_mangle]
pub extern "C" fn vec2d_add(v1: *mut Vec2d, v2: *mut Vec2d) -> *mut Vec2d {
    let v1:&Vec2d = unsafe { &*(&*v1).borrow() };
    let v2:&Vec2d = unsafe { &*(&*v2).borrow() };
    let result = Vec2d{x: v1.x+v2.x, y: v1.y+v2.y};
    Box::into_raw(Box::new(result))
}


#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}
