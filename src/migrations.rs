use std::fs;
use std::io;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

/// Creates a Diesel migration folder with `up.sql` and `down.sql` files.
///
/// The migration folder is named in Diesel's expected format:
/// `YYYY-MM-DD-HHMMSS-XXXX_migration_name`.
///
/// This helper is useful when you want migration creation to happen from code
/// while still keeping SQL migration files in source control.
pub fn generate_migration(
    migrations_dir: impl AsRef<Path>,
    migration_name: &str,
    up_sql: &str,
    down_sql: &str,
) -> io::Result<PathBuf> {
    let migrations_dir = migrations_dir.as_ref();
    fs::create_dir_all(migrations_dir)?;

    let timestamp = migration_timestamp();
    let sequence = next_sequence_for_timestamp(migrations_dir, &timestamp)?;
    let sanitized_name = sanitize_migration_name(migration_name);
    let dir_name = format!("{}-{:04}_{}", timestamp, sequence, sanitized_name);
    let migration_path = migrations_dir.join(dir_name);

    fs::create_dir(&migration_path)?;
    fs::write(migration_path.join("up.sql"), up_sql)?;
    fs::write(migration_path.join("down.sql"), down_sql)?;

    Ok(migration_path)
}

fn migration_timestamp() -> String {
    let secs = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_or(0, |duration| duration.as_secs());
    secs.to_string()
}

fn next_sequence_for_timestamp(migrations_dir: &Path, timestamp: &str) -> io::Result<u16> {
    let mut max_sequence: Option<u16> = None;

    for entry in fs::read_dir(migrations_dir)? {
        let entry = entry?;
        if !entry.file_type()?.is_dir() {
            continue;
        }

        let file_name = entry.file_name();
        let file_name = file_name.to_string_lossy();

        if !file_name.starts_with(timestamp) {
            continue;
        }

        // Expected prefix: YYYY-MM-DD-HHMMSS-XXXX_
        let after_timestamp = &file_name[timestamp.len()..];
        if !after_timestamp.starts_with('-') {
            continue;
        }

        let remainder = &after_timestamp[1..];
        let Some((sequence_text, _name)) = remainder.split_once('_') else {
            continue;
        };

        if let Ok(sequence) = sequence_text.parse::<u16>() {
            max_sequence = Some(max_sequence.map_or(sequence, |current| current.max(sequence)));
        }
    }

    Ok(max_sequence.map_or(0, |s| s.saturating_add(1)))
}

fn sanitize_migration_name(name: &str) -> String {
    let mut output = String::new();
    let mut previous_was_separator = false;

    for ch in name.chars() {
        if ch.is_ascii_alphanumeric() {
            output.push(ch.to_ascii_lowercase());
            previous_was_separator = false;
        } else if !previous_was_separator {
            output.push('_');
            previous_was_separator = true;
        }
    }

    let output = output.trim_matches('_').to_string();
    if output.is_empty() {
        "migration".to_string()
    } else {
        output
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::{SystemTime, UNIX_EPOCH};

    fn temp_migration_dir() -> PathBuf {
        let unique = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_or(0, |duration| duration.as_nanos());
        let dir = std::env::temp_dir().join(format!("diesel_demo_migrations_{unique}"));
        fs::create_dir_all(&dir).expect("create temp migration dir");
        dir
    }

    #[test]
    fn sanitize_name_replaces_separators() {
        assert_eq!(
            sanitize_migration_name("Create Posts Table!"),
            "create_posts_table"
        );
        assert_eq!(sanitize_migration_name("***"), "migration");
    }

    #[test]
    fn sequence_increments_for_existing_timestamp() {
        let dir = temp_migration_dir();

        fs::create_dir(dir.join("1234567890-0000_create_posts")).unwrap();
        fs::create_dir(dir.join("1234567890-0002_add_index")).unwrap();

        let seq = next_sequence_for_timestamp(&dir, "1234567890").unwrap();
        assert_eq!(seq, 3);

        fs::remove_dir_all(dir).ok();
    }

    #[test]
    fn generate_writes_migration_files() {
        let temp = temp_migration_dir();
        let path = generate_migration(
            &temp,
            "Add comments table",
            "CREATE TABLE comments (id SERIAL PRIMARY KEY);",
            "DROP TABLE comments;",
        )
        .expect("migration generated");

        assert!(path.exists());
        assert_eq!(
            fs::read_to_string(path.join("up.sql")).unwrap(),
            "CREATE TABLE comments (id SERIAL PRIMARY KEY);"
        );
        assert_eq!(
            fs::read_to_string(path.join("down.sql")).unwrap(),
            "DROP TABLE comments;"
        );

        fs::remove_dir_all(temp).ok();
    }
}
