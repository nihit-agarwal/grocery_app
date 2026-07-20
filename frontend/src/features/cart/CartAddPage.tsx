import { Paper, Stack, Title, Text, Button, Select, TextInput, NumberInput, Alert } from "@mantine/core";
import { useEffect, useMemo, useState, type SubmitEvent } from "react";
import { http } from "../../services/http";
import { useNavigate, useParams } from "react-router-dom";
import type { itemListResponse, catalogItem }  from "../catalog/CatalogPage"
export default function CartAddPage() {
    // item_id, purchased_on", "expiry_date", "qty", "unit
    const [error, setError] = useState("");
    const [itemId, setItemId] = useState("");
    const [purchasedOn, setPurchasedOn] = useState("");
    const [expiry, setExpiry] = useState("");
    const [qty, setQty] = useState<number>(0);
    const [unit, setUnit] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [loading, setLoading] = useState(true);
    const [items, setItems] = useState<catalogItem[]>([]);
    const navigate = useNavigate();
    

    const {householdid} = useParams();

    const unitTypes = [{value: "l", label: "l"},
        {value: "kg", label: "kg"}
    ];

    const catalogOptions = useMemo(() => 
        items.map((item) => ({
            value: String(item.item_id),
            label: `${item.item_name} (${item.item_type})`
        })), [items]
    );
    
    useEffect(() => {
        async function loadCatalog() {
            try {
                setError("");
                const response = await http.get<itemListResponse>("/households/" + householdid + "/catalog/all");
                setItems(response.data.items);
                

            } catch {
                setError("Could not load your catalog right now")
            } finally {
                setLoading(false);
            }
        }
        loadCatalog();
    }, [])

    // Handler to send request to add item to inventory

    async function handleSubmit(e: SubmitEvent<HTMLFormElement>) {
        e.preventDefault();
        setError("");
        setSubmitting(true);

        // Data packet to send in post req
        const data = {"item": itemId, "qty_needed": qty, "unit": unit}

        try {
            await http.post(`/households/${householdid}/cart`, data);
            navigate(`/households/${householdid}/cart`, { replace: true});
        } catch {
            setError("Unable to add item to inventory");
        } finally {
            setSubmitting(false);
        }

    }

    async function cancelAddition() {
        navigate(`/households/${householdid}/cart`, { replace: true});

    }
    return (
        <main className="page">
            <Paper withBorder shadow="md" radius="xl" p="xl" maw={760} mx="auto">
                <Stack gap="lg">
                    <div>
                        <Text c="green.7" fw={700} tt="uppercase" size="sm">
                            Grocery App
                        </Text>
                        <Title order={1}> Add Item</Title>
                        <Text c="dimmed">
                            Enter details to add item to cart.
                        </Text>
                    </div>

                    <form onSubmit={handleSubmit}>
                        <Stack gap="lg">

                        
                            <Select
                            label="Item Name"
                            placeholder="Search item"
                            searchable
                            data={catalogOptions}
                            value={itemId}
                            onChange={(value) => setItemId(value ?? "")}
                            nothingFoundMessage="No matching item"
                            required
                            />


                            <Stack gap="md" justify="flex-start" style={{flexDirection: "row"}}>

                                <NumberInput
                                label="Quantity"
                                value={qty}
                                onChange={(value) => setQty(typeof value === "number" ? value : 0)}
                                min={0.01}
                                step={0.01}
                                decimalScale={2}
                                required
                                />

                                <Select
                                label="Unit"
                                data={unitTypes}
                                value={unit}
                                onChange={(e) => setUnit(e || "")}
                                required
                                />

                            </Stack>
                            
                            

                            <Stack gap="md" justify="flex-end" style={{ flexDirection: "row" }}>
                                <Button onClick={cancelAddition} size="sm" radius="md" color="red">Cancel</Button>
                                <Button type="submit" loading={submitting} size="sm" radius="md">
                                    {submitting ? "Adding": "Add"}
                                </Button>
                            </Stack>

                            {error ? (
                                <Alert color="red" title="Could not add item">
                                    {error}
                                </Alert>
                            ): null}

                        </Stack>

                    </form>
                </Stack>
            </Paper>
        </main>
    )
}