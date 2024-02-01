import winreg


def deleteNavicatSpecKey():
    navicatKeyName = r"Software\PremiumSoft\NavicatPremium"
    navicatKey = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, navicatKeyName, 0, winreg.KEY_ALL_ACCESS
    )

    deleteKeyName = "Registration15XCS"
    for idx in range(winreg.QueryInfoKey(navicatKey)[0]):
        subKeyName = winreg.EnumKey(navicatKey, idx)
        if subKeyName == deleteKeyName:
            print(f"found key: {deleteKeyName}, delete...")
            winreg.DeleteKey(navicatKey, subKeyName)
            # 删除后中断循环, 否则遍历会索引异常
            break


def deleteClsidSpecKey():
    clsidKeyName = r"Software\Classes\CLSID"
    # 删除 CLSID 下的仅包含 Info 子项的项
    clsidKey = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, clsidKeyName, 0, winreg.KEY_ALL_ACCESS
    )

    deleteKeyName = "Info"
    for idx in range(winreg.QueryInfoKey(clsidKey)[0]):
        subKeyName = winreg.EnumKey(clsidKey, idx)
        subKey = winreg.OpenKey(clsidKey, subKeyName)
        if winreg.QueryInfoKey(subKey)[0] == 1:
            if winreg.EnumKey(subKey, 0) == deleteKeyName:
                print(f"found info key: {subKeyName}, delete...")
                # delete info in subKey
                winreg.DeleteKey(subKey, deleteKeyName)
                # delete subKey
                winreg.DeleteKey(clsidKey, subKeyName)
                # 删除后中断循环, 否则遍历会索引异常
                break


def main():
    deleteClsidSpecKey()
    deleteNavicatSpecKey()


if __name__ == "__main__":
    main()
