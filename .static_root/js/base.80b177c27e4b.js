var path = document.location.pathname;

if (path.includes('bookmap')) {
    result = '책방지도'
} else if (path.includes('board')) {
    result = '문화프로그램'
} else if (path.includes('guide')) {
    result = '출판물 제작 가이드'
} else if (path.includes('mypage')) {
    result = '마이페이지'
} else if (path.includes('signup')) {
    result = '회원가입'
} else if (path.includes('login')) {
    result = '로그인'
} else if (path.includes('storedetail')) {
    result = '책방지도'
} else if (path.includes('ranking')) {
    result = '랭킹'
}
else {
    result = '동네북'
}

document.write(result)
