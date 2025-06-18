#!/bin/bash

# CLAUDE.md 上書き更新スクリプト
# @.claude/*.md を元に @CLAUDE.md を完全に上書きする

#!/bin/bash

# CLAUDE.md タグ更新スクリプト
# @.claude/*.md を元に @CLAUDE.md の特定タグ内容を更新する

set -e

# タグ内容を更新する関数
update_tag_content() {
    local source_file="$1"
    local tag_name="$2" 
    local target_file="$3"
    local temp_update=$(mktemp)
    
    # 新しい内容を読み込み
    local new_content
    new_content=$(cat "$source_file")
    
    # タグが存在するかチェック
    if grep -q "<!-- START:$tag_name -->" "$target_file" && grep -q "<!-- END:$tag_name -->" "$target_file"; then
        # 既存のタグ内容を更新
        awk -v tag="$tag_name" -v content="$new_content" '
        BEGIN { in_tag = 0 }
        /<!-- START:/ && $0 ~ "<!-- START:" tag " -->" { 
            print $0
            print content
            in_tag = 1
            next
        }
        /<!-- END:/ && $0 ~ "<!-- END:" tag " -->" && in_tag {
            print $0
            in_tag = 0
            next
        }
        !in_tag { print }
        ' "$target_file" > "$temp_update"
    else
        # タグが存在しない場合は末尾に追加
        {
            cat "$target_file"
            echo ""
            echo "<!-- START:$tag_name -->"
            echo "$new_content"
            echo "<!-- END:$tag_name -->"
        } > "$temp_update"
    fi
    
    cp "$temp_update" "$target_file"
    rm -f "$temp_update"
}

echo "🔄 CLAUDE.md のタグ内容を更新中..."

# 一時ファイル
TEMP_FILE=$(mktemp)
trap "rm -f $TEMP_FILE" EXIT

# CLAUDE.md が存在しない場合は作成
if [[ ! -f "CLAUDE.md" ]]; then
    echo "📝 CLAUDE.md が存在しないため新規作成します"
    > CLAUDE.md
fi

# CLAUDE.md をコピー
cp CLAUDE.md "$TEMP_FILE"

echo "📝 .claude/ の .md ファイルからタグ内容を更新中..."

# 現在存在するファイル名のリストを取得
existing_files=()
for md_file in .claude/*.md; do
    if [[ -f "$md_file" && ! "$(basename "$md_file")" =~ ^_ ]]; then
        filename=$(basename "$md_file" .md)
        existing_files+=("$filename")
    fi
done

# CLAUDE.md から存在しないタグを削除
echo "🗑️  削除されたファイルに対応するタグを削除中..."
current_tags=$(grep -o '<!-- START:[^[:space:]]*' CLAUDE.md | sed 's/<!-- START://' || true)
for tag in $current_tags; do
    # 対応するファイルが存在しない場合はタグを削除
    if [[ ! " ${existing_files[@]} " =~ " ${tag} " ]]; then
        echo "  - $tag タグを削除"
        # タグとその内容を削除
        awk -v tag="$tag" '
        BEGIN { in_tag = 0 }
        /<!-- START:/ && $0 ~ "<!-- START:" tag " -->" { 
            in_tag = 1
            next
        }
        /<!-- END:/ && $0 ~ "<!-- END:" tag " -->" && in_tag {
            in_tag = 0
            next
        }
        !in_tag { print }
        ' "$TEMP_FILE" > "$TEMP_FILE.tmp"
        mv "$TEMP_FILE.tmp" "$TEMP_FILE"
    fi
done

# .claude/ の .md ファイルを処理（_*.md は除外）
for md_file in .claude/*.md; do
    # ファイルが存在し、_で始まらない場合のみ処理
    if [[ -f "$md_file" && ! "$(basename "$md_file")" =~ ^_ ]]; then
        filename=$(basename "$md_file" .md)
        echo "  - $filename タグの内容を更新"
        
        # タグで囲まれた部分を更新する
        update_tag_content "$md_file" "$filename" "$TEMP_FILE"
    fi
done

# init タグがある場合は、その内容を一番上に移動
if grep -q "<!-- START:init -->" "$TEMP_FILE"; then
    echo "📝 init タグの内容を一番上に移動中..."
    
    # init タグの内容を抽出
    INIT_CONTENT=$(awk '
    /<!-- START:init -->/ { in_tag = 1; next }
    /<!-- END:init -->/ && in_tag { in_tag = 0; next }
    in_tag { print }
    ' "$TEMP_FILE")
    
    # init タグを削除したファイルを作成
    awk '
    /<!-- START:init -->/ { in_tag = 1; next }
    /<!-- END:init -->/ && in_tag { in_tag = 0; next }
    !in_tag { print }
    ' "$TEMP_FILE" > "$TEMP_FILE.no_init"
    
    # init の内容を一番上に、その他のタグを下に配置
    {
        echo "$INIT_CONTENT"
        echo ""
        cat "$TEMP_FILE.no_init"
    } > "$TEMP_FILE.final"
    
    rm -f "$TEMP_FILE.no_init"
    cp "$TEMP_FILE.final" CLAUDE.md
    rm -f "$TEMP_FILE.final"
else
    # init タグがない場合は通常の処理
    cp "$TEMP_FILE" CLAUDE.md
fi

echo "✅ CLAUDE.md のタグ更新が完了しました"