import {
    QueryClient,
    QueryClientProvider,
} from "@tanstack/react-query";

import {
    ReactQueryDevtools,
} from "@tanstack/react-query-devtools";

import { ReactNode } from "react";

type QueryProviderProps = {
    children: ReactNode;
};

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            retry: 2,

            staleTime:
                1000 *
                60 *
                5,

            gcTime:
                1000 *
                60 *
                30,

            refetchOnWindowFocus:
                false,

            refetchOnReconnect:
                true,

            refetchOnMount:
                false,
        },

        mutations: {
            retry: 1,
        },
    },
});

export default function QueryProvider({
    children,
}: QueryProviderProps) {
    return (
        <QueryClientProvider
            client={queryClient}
        >
            {children}

            <ReactQueryDevtools
                initialIsOpen={false}
            />
        </QueryClientProvider>
    );
}
