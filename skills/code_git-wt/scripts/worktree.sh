#!/bin/bash

# 通用 Git Worktree 管理脚本
# 适用于任何 Git 项目的多分支并行开发

set -e

# ========== 配置加载 ==========

# 默认配置
DEFAULT_WORKTREE_BASE="../"
DEFAULT_BRANCH_PREFIX="dev"
DEFAULT_SHARED_ITEMS=(
  ".env"
  ".env.local"
)
DEFAULT_AUTO_CREATE_SHARED="false"

# 从配置文件加载（如果存在）
load_config() {
  local config_file=".worktree.config"

  if [ -f "$config_file" ]; then
    # shellcheck source=/dev/null
    source "$config_file"
  fi

  # 自动检测项目名称
  if [ -z "$PROJECT_NAME" ]; then
    # 优先从 git remote 获取
    local remote_url=$(git config --get remote.origin.url 2>/dev/null || echo "")
    if [ -n "$remote_url" ]; then
      PROJECT_NAME=$(basename "$remote_url" .git)
    else
      # 从目录名获取
      PROJECT_NAME=$(basename "$(git rev-parse --show-toplevel)")
    fi
  fi

  # 使用默认值（如果未配置）
  WORKTREE_BASE="${WORKTREE_BASE:-$DEFAULT_WORKTREE_BASE}"
  BRANCH_PREFIX="${BRANCH_PREFIX:-$DEFAULT_BRANCH_PREFIX}"
  AUTO_CREATE_SHARED="${AUTO_CREATE_SHARED:-$DEFAULT_AUTO_CREATE_SHARED}"

  # 如果未配置共享项，使用默认值
  if [ ${#SHARED_ITEMS[@]} -eq 0 ]; then
    SHARED_ITEMS=("${DEFAULT_SHARED_ITEMS[@]}")
  fi
}

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_info() {
  echo -e "${GREEN}✓${NC} $1"
}

print_warn() {
  echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
  echo -e "${RED}✗${NC} $1"
}

print_step() {
  echo -e "${BLUE}▸${NC} $1"
}

print_header() {
  echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${CYAN}$1${NC}"
  echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# ========== 帮助信息 ==========

show_help() {
  cat <<EOF
通用 Git Worktree 管理脚本

使用方法: $0 <command> [options]

命令:
  init                  初始化配置文件 (.worktree.config)
  add <name>            创建新的 worktree
  remove <name>         删除指定的 worktree
  list                  列出所有 worktree
  status                显示共享文件状态
  clean                 清理所有 worktree（保留主目录）
  config                显示当前配置
  help                  显示此帮助信息

名称示例:
  feature-auth    -> 创建 ${BRANCH_PREFIX}/feature-auth 分支
  bugfix-123      -> 创建 ${BRANCH_PREFIX}/bugfix-123 分支
  experiment      -> 创建 ${BRANCH_PREFIX}/experiment 分支

当前配置:
  项目名称: ${PROJECT_NAME}
  Worktree 基础路径: ${WORKTREE_BASE}
  分支前缀: ${BRANCH_PREFIX}
  共享项数量: ${#SHARED_ITEMS[@]}
  自动创建共享项: ${AUTO_CREATE_SHARED}

批量操作:
  $0 add name1 name2 name3     批量创建
  $0 remove name1 name2        批量删除

示例:
  $0 init                      初始化配置
  $0 add feature-login         创建登录功能分支
  $0 list                      查看所有 worktree
  $0 status                    检查共享文件状态
  $0 remove feature-login      删除 worktree
  $0 clean                     清理所有 worktree

提示:
  - 脚本可直接用绝对路径执行, 不要求复制到仓库
  - 默认不自动创建共享项文件或目录, 需要时设置 AUTO_CREATE_SHARED=true
EOF
}

# ========== 初始化配置 ==========

init_config() {
  local config_file=".worktree.config"

  if [ -f "$config_file" ]; then
    print_warn "配置文件已存在: $config_file"
    read -p "是否覆盖? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      print_info "取消初始化"
      exit 0
    fi
  fi

  # 自动检测项目名称
  local detected_name
  local remote_url=$(git config --get remote.origin.url 2>/dev/null || echo "")
  if [ -n "$remote_url" ]; then
    detected_name=$(basename "$remote_url" .git)
  else
    detected_name=$(basename "$(git rev-parse --show-toplevel)")
  fi

  cat > "$config_file" <<'EOF'
# Git Worktree 配置文件
# 此文件应添加到 .gitignore（如果包含本地路径）

# 项目名称（用于生成 worktree 目录名）
# 格式: ${PROJECT_NAME}-${name}
PROJECT_NAME="<PROJECT_NAME>"

# Worktree 基础路径（相对于当前仓库）
# 建议: "../" (与主仓库并列)
WORKTREE_BASE="../"

# 分支前缀
# 所有 worktree 分支将使用此前缀，如: dev/feature-auth
BRANCH_PREFIX="dev"

# 需要共享的文件和目录（软链接方式）
# 所有 worktree 会自动链接到主目录，实现配置同步
SHARED_ITEMS=(
  ".env"                    # 环境变量
  ".env.local"              # 本地环境变量
  # 根据项目需要添加更多共享项
  # ".vscode/settings.json" # VS Code 设置
  # "config/local.json"     # 本地配置
  # "docs/local"            # 本地文档
)

# 是否允许自动创建共享项（默认 false，避免改动仓库内容）
AUTO_CREATE_SHARED="false"

# 注意：
# 1. 共享项路径相对于项目根目录
# 2. 可以是文件或目录
# 3. 主目录中不存在的项会被跳过
# 4. 软链接会自动创建，修改任意 worktree 中的共享文件会同步到所有 worktree
EOF

  # 替换项目名称
  sed -i.bak "s/<PROJECT_NAME>/$detected_name/" "$config_file"
  rm -f "${config_file}.bak"

  print_info "配置文件已创建: $config_file"
  print_info "检测到的项目名称: $detected_name"
  echo ""
  print_step "下一步:"
  echo "  1. 编辑 $config_file 调整配置（可选）"
  echo "  2. 运行 '$0 add <name>' 创建第一个 worktree"
  echo ""
  print_warn "建议将 $config_file 添加到 .gitignore（如果包含本地路径）"
}

# ========== 显示配置 ==========

show_config() {
  print_header "当前配置"
  echo ""
  echo "项目名称:        $PROJECT_NAME"
  echo "Worktree 路径:   $WORKTREE_BASE"
  echo "分支前缀:        $BRANCH_PREFIX"
  echo "配置文件:        $([ -f .worktree.config ] && echo "已加载" || echo "使用默认配置")"
  echo "自动创建共享项: $AUTO_CREATE_SHARED"
  echo ""
  print_step "共享项 (${#SHARED_ITEMS[@]} 个):"
  for item in "${SHARED_ITEMS[@]}"; do
    echo "  - $item"
  done
  echo ""
}

# ========== 确保主目录文件 ==========

ensure_main_files() {
  local main_path=$(git rev-parse --show-toplevel)

  if [ "$AUTO_CREATE_SHARED" != "true" ]; then
    print_warn "默认零侵入模式: 主目录缺失的共享项将被跳过"
    return 0
  fi

  # 如果 .env 不存在，从 .env.example 复制
  if [ ! -f "$main_path/.env" ] && [ -f "$main_path/.env.example" ]; then
    print_step "主目录缺少 .env，正在从 .env.example 复制..."
    cp "$main_path/.env.example" "$main_path/.env"
    print_info ".env 文件已创建"
    print_warn "请编辑 .env 文件填入实际配置"
  fi

  # 确保共享目录存在
  for item in "${SHARED_ITEMS[@]}"; do
    local source_path="$main_path/$item"

    # 跳过文件（只创建目录）
    if [[ "$item" == *.* ]] || [[ "$item" == .* ]] && [[ ! "$item" =~ / ]]; then
      continue
    fi

    # 创建不存在的目录
    if [ ! -e "$source_path" ]; then
      mkdir -p "$source_path"
      print_info "创建目录: $item"
    fi
  done
}

# ========== 计算相对路径 ==========

get_relative_path() {
  local source=$1
  local target=$2

  # 检查 python3 是否可用
  if command -v python3 &> /dev/null; then
    python3 -c "import os.path; print(os.path.relpath('$source', '$target'))"
  elif command -v python &> /dev/null; then
    python -c "import os.path; print(os.path.relpath('$source', '$target'))"
  else
    print_error "需要 Python 来计算相对路径，但未找到 python 或 python3"
    exit 1
  fi
}

# ========== 创建软链接 ==========

create_symlinks() {
  local worktree_path=$1
  local main_path=$(git rev-parse --show-toplevel)

  echo ""
  print_step "正在创建软链接（共享配置）..."

  local link_count=0
  local skip_count=0

  for item in "${SHARED_ITEMS[@]}"; do
    local source_path="$main_path/$item"
    local target_path="$worktree_path/$item"
    local target_dir=$(dirname "$target_path")

    # 如果源文件/目录不存在，跳过
    if [ ! -e "$source_path" ]; then
      print_warn "跳过 $item（主目录中不存在）"
      ((skip_count++))
      continue
    fi

    # 确保目标目录存在
    mkdir -p "$target_dir"

    # 如果目标已存在，先删除
    if [ -e "$target_path" ] || [ -L "$target_path" ]; then
      rm -rf "$target_path"
    fi

    # 计算相对路径
    local relative_path=$(get_relative_path "$source_path" "$target_dir")

    # 创建软链接
    ln -s "$relative_path" "$target_path"

    if [ -L "$target_path" ]; then
      print_info "已链接: $item"
      ((link_count++))
    else
      print_error "链接失败: $item"
    fi
  done

  echo ""
  print_info "软链接创建完成: $link_count 个成功，$skip_count 个跳过"

  if [ $skip_count -gt 0 ]; then
    print_warn "部分文件不存在，可在主目录创建后自动同步到所有 worktree"
  fi
}

# ========== 创建 Worktree ==========

create_worktree() {
  local name=$1
  local branch_name="${BRANCH_PREFIX}/${name}"
  local worktree_path="${WORKTREE_BASE}${PROJECT_NAME}-${name}"

  if [ -z "$name" ]; then
    print_error "请指定 worktree 名称"
    show_help
    exit 1
  fi

  # 检查 worktree 目录是否已存在
  if [ -d "$worktree_path" ]; then
    print_error "Worktree 目录已存在: $worktree_path"
    exit 1
  fi

  # 确保主目录的必要文件存在
  ensure_main_files

  # 检查分支是否已存在
  if git rev-parse --verify "$branch_name" >/dev/null 2>&1; then
    print_warn "分支 $branch_name 已存在，将使用现有分支"
    git worktree add "$worktree_path" "$branch_name"
  else
    print_info "创建新分支: $branch_name"
    # 自动检测默认分支
    local default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
    git worktree add -b "$branch_name" "$worktree_path" "$default_branch"
  fi

  print_info "Worktree 创建成功!"
  print_info "路径: $worktree_path"
  print_info "分支: $branch_name"

  # 创建软链接
  create_symlinks "$worktree_path"

  echo ""
  print_header "完成"
  echo ""
  print_step "进入工作目录:"
  echo "  cd $worktree_path"
  echo ""
  print_step "共享配置说明:"
  echo "  - 默认零侵入: 不自动在主仓库创建共享项"
  echo "  - 存在的共享项会通过软链接同步到所有 worktree"
  echo "  - 查看共享状态: $0 status"
  echo ""
}

# ========== 删除 Worktree ==========

remove_worktree() {
  local name=$1
  local branch_name="${BRANCH_PREFIX}/${name}"
  local worktree_path="${WORKTREE_BASE}${PROJECT_NAME}-${name}"

  if [ -z "$name" ]; then
    print_error "请指定 worktree 名称"
    show_help
    exit 1
  fi

  if [ ! -d "$worktree_path" ]; then
    print_error "Worktree 不存在: $worktree_path"
    exit 1
  fi

  read -p "确认删除 worktree '$name'? (y/N) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    git worktree remove "$worktree_path"
    print_info "Worktree 已删除: $worktree_path"

    read -p "是否同时删除分支 '$branch_name'? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      git branch -D "$branch_name" 2>/dev/null || print_warn "分支不存在或已删除"
      print_info "分支已删除: $branch_name"
    fi
  else
    print_info "取消删除"
  fi
}

# ========== 列出 Worktree ==========

list_worktrees() {
  print_header "所有 Worktree"
  echo ""
  git worktree list
  echo ""
}

# ========== 显示状态 ==========

show_status() {
  local main_path=$(git rev-parse --show-toplevel)

  print_header "共享文件状态"
  echo ""

  print_step "主目录路径: $main_path"
  echo ""

  # 检查主目录的共享文件
  print_step "主目录共享文件:"
  for item in "${SHARED_ITEMS[@]}"; do
    local source_path="$main_path/$item"
    if [ -e "$source_path" ]; then
      if [ -d "$source_path" ]; then
        print_info "$item (目录)"
      else
        print_info "$item (文件)"
      fi
    else
      print_warn "$item (不存在)"
    fi
  done

  # 检查所有 worktree 的链接状态
  echo ""
  print_step "各 worktree 链接状态:"

  git worktree list --porcelain | grep "worktree " | cut -d' ' -f2 | while read -r worktree_path; do
    # 跳过主目录
    if [ "$worktree_path" = "$main_path" ]; then
      continue
    fi

    local worktree_name=$(basename "$worktree_path")
    echo ""
    echo "  📁 $worktree_name:"

    for item in "${SHARED_ITEMS[@]}"; do
      local target_path="$worktree_path/$item"
      if [ -L "$target_path" ]; then
        local link_target=$(readlink "$target_path")
        echo "    ✓ $item -> $link_target"
      elif [ -e "$target_path" ]; then
        echo "    ⚠ $item (存在但不是软链接)"
      else
        echo "    ✗ $item (不存在)"
      fi
    done
  done

  echo ""
  print_info "提示: 所有软链接指向主目录，修改任意处会自动同步"
  echo ""
}

# ========== 清理所有 Worktree ==========

clean_all_worktrees() {
  local main_path=$(git rev-parse --show-toplevel)

  read -p "确认清理所有 worktree (保留主目录)? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "取消清理"
    exit 0
  fi

  git worktree list --porcelain | grep "worktree " | cut -d' ' -f2 | while read -r worktree_path; do
    if [ "$worktree_path" != "$main_path" ]; then
      print_info "删除: $worktree_path"
      git worktree remove "$worktree_path" --force
    fi
  done

  print_info "所有 worktree 已清理"

  read -p "是否删除所有 ${BRANCH_PREFIX}/* 分支? (y/N) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    git branch | grep "^  ${BRANCH_PREFIX}/" | sed 's/^  //' | while read -r branch; do
      print_info "删除分支: $branch"
      git branch -D "$branch"
    done
  fi
}

# ========== 批量操作 ==========

batch_create() {
  local total=$#
  local success=0
  local failed=0

  echo ""
  print_step "批量创建 $total 个 worktree..."
  echo ""

  for name in "$@"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_step "[$((success + failed + 1))/$total] 创建: $name"
    echo ""

    if create_worktree "$name"; then
      ((success++))
    else
      ((failed++))
    fi
    echo ""
  done

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  print_info "==== 批量创建完成 ===="
  print_info "成功: $success 个"
  if [ $failed -gt 0 ]; then
    print_warn "失败: $failed 个"
    return 1
  fi
  return 0
}

batch_remove() {
  local total=$#

  echo ""
  print_info "将要删除的 worktree:"
  for name in "$@"; do
    echo "  - $name"
  done
  echo ""

  read -p "确认批量删除以上 worktree? (y/N) " -n 1 -r
  echo
  [[ ! $REPLY =~ ^[Yy]$ ]] && print_info "取消删除" && exit 0

  read -p "是否同时删除对应的分支? (y/N) " -n 1 -r
  echo
  local delete_branch=$REPLY

  local success=0
  local failed=0

  echo ""
  for name in "$@"; do
    local branch_name="${BRANCH_PREFIX}/${name}"
    local worktree_path="${WORKTREE_BASE}${PROJECT_NAME}-${name}"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_step "[$((success + failed + 1))/$total] 删除: $name"

    if [ ! -d "$worktree_path" ]; then
      print_warn "不存在: $worktree_path"
      ((failed++))
      continue
    fi

    if git worktree remove "$worktree_path" 2>/dev/null; then
      print_info "已删除: $worktree_path"
      [[ $delete_branch =~ ^[Yy]$ ]] && git branch -D "$branch_name" 2>/dev/null && print_info "分支已删除"
      ((success++))
    else
      print_error "删除失败"
      ((failed++))
    fi
    echo ""
  done

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  print_info "==== 批量删除完成 ===="
  print_info "成功: $success 个"
  if [ $failed -gt 0 ]; then
    print_warn "失败: $failed 个"
    return 1
  fi
  return 0
}

# ========== 主逻辑 ==========

# 检查是否在 git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  print_error "当前目录不是 git 仓库"
  exit 1
fi

# 加载配置
load_config

# 命令分发
case "${1:-help}" in
  init)
    init_config
    ;;
  add)
    shift
    if [ $# -eq 0 ]; then
      print_error "请提供至少一个 worktree 名称"
      exit 1
    elif [ $# -gt 1 ]; then
      batch_create "$@"
    else
      create_worktree "$1"
    fi
    ;;
  remove|rm)
    shift
    if [ $# -eq 0 ]; then
      print_error "请提供至少一个 worktree 名称"
      exit 1
    elif [ $# -gt 1 ]; then
      batch_remove "$@"
    else
      remove_worktree "$1"
    fi
    ;;
  list|ls)
    list_worktrees
    ;;
  status|st)
    show_status
    ;;
  clean)
    clean_all_worktrees
    ;;
  config|cfg)
    show_config
    ;;
  help|--help|-h)
    show_help
    ;;
  *)
    print_error "未知命令: $1"
    echo ""
    show_help
    exit 1
    ;;
esac
