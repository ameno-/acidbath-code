#!/usr/bin/env bun
/**
 * Usage:
 *   bun db-agent.ts --query "SELECT * FROM users"
 *   import { query } from "./db-agent.ts"
 */

import mysql from "mysql2/promise";
import { parseArgs } from "util";

type Connection = mysql.Connection;
let _db: Connection | null = null;

async function getConnection(): Promise<Connection> {
  if (!_db) {
    _db = await mysql.createConnection({
      host: Bun.env.MYSQL_HOST || "localhost",
      user: Bun.env.MYSQL_USER || "root",
      password: Bun.env.MYSQL_PASS || "",
      database: Bun.env.MYSQL_DB || "mysql",
    });
  }
  return _db;
}

export async function query(sql: string): Promise<any[]> {
  const db = await getConnection();
  const [rows] = await db.execute(sql);
  return Array.isArray(rows) ? rows : [];
}

export async function close(): Promise<void> {
  if (_db) {
    await _db.end();
    _db = null;
  }
}

// CLI mode
if (import.meta.main) {
  const { values } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      query: { type: "string", short: "q" },
    },
  });

  if (!values.query) {
    console.error("Usage: bun db-agent.ts --query 'SELECT ...'");
    process.exit(1);
  }

  try {
    const results = await query(values.query);
    console.log(JSON.stringify(results, null, 2));
  } finally {
    await close();
  }
}
