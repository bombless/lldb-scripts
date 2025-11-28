import lldb

def option_summary(valobj, internal_dict):
    """
    针对 Rust enum Option<T> 的格式化器
    结构:
      $variants$
        $variant$0 (None): $discr$ = 0
        $variant$1 (Some): $discr$ = 1, value.__0 = 实际值
    """
    try:
        variants = valobj.GetChildMemberWithName("$variants$")
        if not variants.IsValid():
            return "<invalid Option>"
        
        # 读取 variant1 的 discriminant 来判断
        variant1 = variants.GetChildMemberWithName("$variant$1")
        discr = variant1.GetChildMemberWithName("$discr$").GetValueAsUnsigned()
        
        if discr == 0:
            return "None"
        else:
            # Some 分支
            value = variant1.GetChildMemberWithName("value")
            inner = value.GetChildMemberWithName("__0")
            
            if inner.IsValid():
                # 优先用 GetValue()，否则用 GetSummary()
                display = inner.GetValue()
                if not display:
                    display = inner.GetSummary()
                if not display:
                    display = str(inner.GetValueAsUnsigned())
                return f"Some({display})"
            return "Some(...)"
            
    except Exception as e:
        return f"<error: {e}>"

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand(
        'type summary add -F option.option_summary -x "^core::option::Option<.+>$"'
    )
    print("✓ Option formatter loaded")
