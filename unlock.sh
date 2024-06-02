#!/bin/bash

# Пути к возможным местоположениям файла daemon.json
paths=(
    "/etc/docker/daemon.json"
    "/var/snap/docker/current/config/daemon.json"
)

# Новая конфигурация для добавления
registry_mirrors='"registry-mirrors": [
    "https://mirror.gcr.io",
    "https://daocloud.io",
    "https://c.163.com/",
    "https://registry.docker-cn.com"
  ]'

# Функция для обновления файла daemon.json
update_daemon_json() {
    local path="$1"
    if [ -f "$path" ]; then
        # Чтение текущей конфигурации
        current_config=$(cat "$path")

        # Удаление последней скобки
        current_config="${current_config%?}"

        # Добавление новой конфигурации
        new_config="$current_config,
    $registry_mirrors
}"

        # Запись новой конфигурации в файл
        echo "$new_config" > "$path"

        # Перезапуск Docker
        if [[ "$path" == "/etc/docker/daemon.json" ]]; then
            sudo systemctl restart docker
        else
            sudo snap restart docker
        fi

        echo "Конфигурация обновлена и Docker перезапущен."
        exit 0
    fi
}

# Поиск файла daemon.json и его обновление
for path in "${paths[@]}"; do
    update_daemon_json "$path"
done

echo "Файл daemon.json не найден ни по одному из путей."
exit 1
