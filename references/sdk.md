# TQX Research TypeScript SDK

Source of truth: `packages/sdk/src/research/api.ts` and `packages/sdk/src/research/schemas.ts`. Install `@tqx-ai/sdk` in a Node.js `>=22.18` project. The public entry point exports `TqxClient`, Research API types, and Valibot schemas.

## Configure the client

Pass an API key and a Qube base URL ending in `/pandaApi`. The client sends authenticated research requests with `X-API-Key`.

```ts
import { TqxClient } from '@tqx-ai/sdk'

const client = new TqxClient({
  apiKey: process.env.TQX_API_KEY!,
  baseUrl: process.env.TQX_BASE_URL!, // e.g. https://gateway.example.com/pandaApi
})
```

The SDK rejects missing API keys or invalid base URLs before calling the gateway. It maps gateway failures to `TqxApiError`, malformed responses to `TqxProtocolError`, network failures to `TqxNetworkError`, and invalid public inputs to `TqxValidationError`.

## API surface

```ts
// Factors
client.research.createFactor({ name, description?, code, codeType: 'python' | 'formula', market: 'hk' | 'us' })
client.research.getFactor(factorId)
client.research.updateFactor(factorId, { name?, description?, code?, codeType?, market? })
client.research.listFactors({ offset?, limit?, market?, keyword? })
client.research.deleteFactor(factorId)

// Factor analyses
client.research.createFactorAnalysis(factorId, {
  name?, periodStart?, periodEnd?, adjustmentCycle?, groupNumber?, factorDirection?
})
client.research.getFactorAnalysis(analysisId)
client.research.cancelFactorAnalysis(analysisId)
client.research.pollFactorAnalysis(analysisId, { interval?, timeout?, progressCallback? })

// Strategies
client.research.createStrategy({ name, description?, code, market, backtest? })
client.research.getStrategy(strategyId)
client.research.updateStrategy(strategyId, {
  name?, description?, code?, market?, versionSummary?, backtest?
})
client.research.listStrategies({ offset?, limit?, market?, keyword? })
client.research.deleteStrategy(strategyId)

// Backtests
client.research.runStrategyBacktest(strategyId, backtest?)
client.research.getBacktest(runId)
client.research.cancelBacktest(runId)
client.research.listBacktests({ offset?, limit?, market?, keyword? })
client.research.pollBacktest(runId, { interval?, timeout?, progressCallback? })
```

`list*` returns `{ items, hasMore, nextOffset }`. Its input has `offset >= 0`, `limit` in `1..100`, optional lower-cased market, and a keyword up to 256 characters. IDs must be positive integers.

## Request types

`periodStart` and `periodEnd` use `YYYY-MM-DD`. `factorDirection` is `0` (negative) or `1` (positive). `groupNumber` is an integer from 2 to 20. `adjustmentCycle` is a positive integer.

```ts
type BacktestParameters = {
  periodStart?: string
  periodEnd?: string
  initBalance?: number // positive integer
  commissionRate?: number // >= 0
  slippage?: number // >= 0
  frequency?: '1d' | '1M'
  symbols?: string[]
}
```

`createFactor` and `createStrategy` require non-empty `name`, `code`, and `market`; factor creation also requires a code type. Update methods require at least one defined field. SDK date validation checks the format only; validate calendar validity and date ordering in the application when calling the SDK directly.

## Polling

Polling defaults to a 2-second interval and 600-second timeout. It calls `progressCallback` for every response and stops only when service status lower-cases to `done`, `failed`, or `cancelled`. With a timeout it returns the most recent result plus `{ cli_status: 'TIMEOUT', timeout_seconds }`; it does not issue cancellation.

```ts
const submitted = await client.research.runStrategyBacktest(123, {
  periodStart: '2026-01-01',
  periodEnd: '2026-03-31',
  initBalance: 1_000_000,
  commissionRate: 1,
  slippage: 0,
  frequency: '1d',
  symbols: ['AAPL.US'],
})

const result = await client.research.pollBacktest(submitted.id, {
  interval: 2,
  timeout: 600,
  progressCallback: (current) => console.error(current.status),
})
```

Do not treat a returned `done` status as an investment conclusion. Preserve the full result, parameters, resource IDs, and request identifiers exposed by errors for reproducibility.
