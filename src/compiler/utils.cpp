#include <string>
#include <codecvt>
#include <locale>

std::string to_utf8(const std::wstring& wstr) {
    static std::wstring_convert<std::codecvt_utf8<wchar_t>> utf8_conv;
    return utf8_conv.to_bytes(wstr);
}
