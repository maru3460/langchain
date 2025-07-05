def disp_message(message):
    """
    Anthropic API のメッセージオブジェクトを見やすく表示する関数なのだ
    
    Args:
        message: Anthropic API から返されるメッセージオブジェクト
    """
    print("=" * 50)
    print("📄 Message オブジェクトの詳細情報")
    print("=" * 50)
    
    for key, value in message.__dict__.items():
        if key == "content":
            print(f"📝 {key}:")
            for i, content_block in enumerate(value):
                print(f"   [{i}] {type(content_block).__name__}")
                if hasattr(content_block, 'text'):
                    # テキストが長い場合は切り詰める
                    text = content_block.text
                    if len(text) > 100:
                        text = text[:100] + "..."
                    print(f"       text: {text}")
                if hasattr(content_block, 'name'):
                    print(f"       tool: {content_block.name}")
                if hasattr(content_block, 'input'):
                    print(f"       input: {content_block.input}")
        elif key == "usage":
            print(f"📊 {key}:")
            for usage_key, usage_value in value.__dict__.items():
                print(f"   {usage_key}: {usage_value}")
        else:
            print(f"🔍 {key}: {value}")
    
    print("=" * 50)
