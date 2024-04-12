# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1

Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

path: tokenB->tokenA->tokenD->tokenC->tokenB, tokenB balance=20.129889

tokenB->tokenA: amountIn=5.0, amountOut=5.655322
tokenA->tokenD: amountIn=5.655322, amountOut=2.458781
tokenD->tokenC: amountIn=2.458781, amountOut=5.088927
tokenC->tokenB: amountIn=5.088927, amountOut=20.129888

## Problem 2

What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

AMM 中的 slippage 指的是交易預期價格與實際執行價格之間的差異。由於 liquidity pool 中的 liquidity 有限，大規模交易可能會對價格產生顯著影響，從而造成 slippage，uniswap v2 也有用一些機制來處理這個問題。

```solidity
 function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external override ensure(deadline) returns (uint[] memory amounts) {
        amounts = UniswapV2Library.getAmountsOut(factory, amountIn, path);
        require(amounts[amounts.length - 1] >= amountOutMin, 'UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT');
        TransferHelper.safeTransferFrom(path[0], msg.sender, UniswapV2Library.pairFor(factory, path[0], path[1]), amounts[0]);
        _swap(amounts, path, to);
    }
```

1. deadline: 限制交易時間，避免價格波動過大
2. amountOutMin: 限制最小交易量，避免價格波動過大
3. require(amounts[amounts.length - 1] >= amountOutMin, 'UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT'): 在交易前檢查最終交易量是否大於最小交易量，避免不可接受的 slippage

## Problem 3

Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

``` solidity
liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);
_mint(address(0), MINIMUM_LIQUIDITY); // permanently lock the first MINIMUM_LIQUIDITY tokens
```

設定 minimum liquidity 並把他 lock 住，以此保持最低限度的 liquidity，避免 liquidity pool 因為 liquidity 過低而導致價格波動過大，或甚至是被完全提走。

## Problem 4

Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

``` solidity
liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
```

維持 token pair 比例：通過這個公式計算的 liquidity，可以盡量讓新提供的 token 從現在的 token pair 比例進行增加。避免因新增 liquidity 而引起的 token 比例的不合理波動。

## Problem 5

What is a sandwich attack, and how might it impact you when initiating a swap?

Sandwich attack 是針對 DEX 用戶執行交易的前置攻擊手法，特別是那些交易尚未被確認的交易，攻擊者先以較高的 fee 發起一個與 victim 相同的交易(front running)，確保他的交易先被處理，從而提高 victim 要購買的資產價格。在 victim 的交易執行後，攻擊者再執行一筆賣出交易，從而在提高的價格上獲利。

victim 可能會因此需要支付更高的價格來完成交易，或者在交易完成後發現自己的交易價格不合理。

## Bonus

path: tokenB->tokenA->tokenD->tokenC->tokenB, tokenB balance=20.129889
